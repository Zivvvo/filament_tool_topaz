#!/usr/bin/python
# Problem with micrograph id
from topaz.utils.data.loader import load_image
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from PIL import Image
import glob
import os
import argparse
from sklearn.neighbors import KDTree

parser = argparse.ArgumentParser(description="Selects a micrograph, finds corresponding box file and ground_truth file, and plots coordinates using"
                                             "the bin factor provided")

parser.add_argument('mrc_dir', help = "directory to the .mrc files")
parser.add_argument('binfactor', default = 1, type = int)
parser.add_argument('directory', default = "", help = "directory to the box file")

parser.add_argument('--ground_truth_directory', help = "directory to the box_file that acts as a reference")
parser.add_argument('--s' , default = None, help = "if set, will save output image to designated path")
parser.add_argument('--radius', default = 20, help="radius for overlapped points", type = int)
parser.add_argument('--assort_color', default = 0, help = "set to 1 if you want helical groups to be displayed in different colors", type = bool)

## load the micrographs for visualization


args = parser.parse_args()

image_dir = args.mrc_dir
binfactor= args.binfactor
directory = args.directory
ground_truth_directory = args.ground_truth_directory
assort_color = args.assort_color

def rebin(arr, new_shape):
    shape = (new_shape[0], arr.shape[0] // new_shape[0],
             new_shape[1], arr.shape[1] // new_shape[1])
    return arr.reshape(shape).mean(-1).mean(1)

def find_matching_box(directory, mrc_name):
    name = os.path.splitext(os.path.basename(mrc_name))
    for file in glob.glob(os.path.join(directory+"*.box")):
        box_name = os.path.splitext(os.path.basename(file))
        if box_name in name:
            return box_name
    raise FileNotFoundError("Cannot find matching box file to "+ mrc_name)

def get_coordinates(directory, name):
    name = name + ".box"
    df = pd.read_csv(os.path.join(directory,name),
                     delimiter = "\t", header = None)
    print(df)
    return (df[0]/binfactor, df[1]/binfactor)

def overlapped_points(Truth, Predictions, radius):
    tree = KDTree(Truth, leaf_size = 2*len(Predictions))
    output = []
    for point in Predictions:
        point_copy = point[np.newaxis, :]
        ind = tree.query_radius(point_copy, r = 15)
        if len(ind) != 0:
            output.append(point)
    return output

images = []
for image in glob.glob(os.path.join(image_dir,'*.mrc')):
    im = np.array(load_image(image))
    images.append(im)

while True:
    try:
        print("There are a total of "+ str(len(images)) + " micrographs to view, please specifiy an index between 0 to "+ str(len(images)-1))
        user_response = input("Enter the index for the micrograph you want to select")

        image_name = os.path.basename(glob.glob(os.path.join(image_dir,'*.mrc'))[int(user_response)])

        im = images[int(user_response)]
        Nx, Ny = im.shape
        binx = round(Nx / binfactor)
        biny = round(Ny / binfactor)
        im_bin = rebin(im, (binx, biny))

        plt.imshow(im_bin, cmap="gray")

        box_file_name = find_matching_box(directory, image_name)

        # x = get_coordinates("/storage2/labusr/20210402_TetraCU428/P10/J22/", name)[0]
        x = get_coordinates(directory, box_file_name)[0]
        # y = get_coordinates("/storage2/labusr/20210402_TetraCU428/P10/J22/", name)[1]
        y = get_coordinates(directory, box_file_name)[1]
        plt.scatter(x, y, marker='.', c='b')

        if (ground_truth_directory is not None):
            truth_box_file_name = find_matching_box(ground_truth_directory, image_name)

            x_g = get_coordinates(ground_truth_directory, truth_box_file_name)[0]
            y_g = get_coordinates(ground_truth_directory, truth_box_file_name)[1]
            plt.scatter(x, y, marker=".", c='r')

            truth = pd.concat([x_g, y_g], axis=1)
            print(truth)
            print(truth.shape)
            prediction = pd.concat([x, y], axis=1)

            truth = truth.to_numpy()
            prediction = prediction.to_numpy()
            overlapped_points = overlapped_points(truth, prediction, int(args.radius))
            overlapped_np = np.asarray(overlapped_points)
            print(overlapped_points)
            print(overlapped_np)

            plt.scatter(overlapped_np[:, 0], overlapped_np[:, 1], c='g')

        plt.gca().set_aspect('equal', adjustable='box')
        # plt.gca().invert_yaxis()

        plt.show()
        if (args.s is not None):
            plt.savefig(os.path.join(args.s, os.path.basename(image_name).replace(".mrc", ""), format="png"))
        plt.close()

        Response = input("Continue? Y/N")

        if (Response == "y" or Response == "Y" ):
            continue
        else:
            break

    except IndexError as e:
        print(e)
        print("Invalid index, continue...")
        continue
    except FileNotFoundError as e:
        print(e)
        continue
