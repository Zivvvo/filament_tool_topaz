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

parser = argparse.ArgumentParser()

parser.add_argument('filename', help = "filename")
parser.add_argument('binfactor', default = 1, type = int)
parser.add_argument('directory', default = "", help = "directory to the box file")


parser.add_argument('--prefix', default = "", help = "prefix of the filename")
parser.add_argument('--suffix', default = "", help = "suffix of the filename")
parser.add_argument('--ground_truth', help = "path to the box_file that acts as a reference")
parser.add_argument('--s' , default = None, help = "if set, will save output image to designated path")
parser.add_argument('--radius', default = 20, help="radius for overlapped points", type = int)
parser.add_argument('--assort_color', default = 0, help = "set to 1 if you want helical groups to be displayed in different colors", type = bool)

## load the micrographs for visualization



args = parser.parse_args()

name = args.filename

im = np.array(load_image(name))

name = os.path.splitext(os.path.basename(name))[0]
prefix = args.prefix
suffix = args.suffix
binfactor= args.binfactor
directory = args.directory

ground_truth = os.path.splitext(args.ground_truth)[0]
assort_color = args.assort_color

def rebin(arr, new_shape):
    shape = (new_shape[0], arr.shape[0] // new_shape[0],
             new_shape[1], arr.shape[1] // new_shape[1])
    return arr.reshape(shape).mean(-1).mean(1)


def get_coordinates(directory, name):
    name = name + ".box"
    df = pd.read_csv(os.path.join(directory,
                                  name.replace(prefix, "").replace(suffix, "")),
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


Nx, Ny = im.shape
binx = round(Nx/binfactor)
biny = round(Ny/binfactor)
im_bin = rebin(im, (binx,biny))

plt.imshow(im_bin, cmap= "gray")



#x = get_coordinates("/storage2/labusr/20210402_TetraCU428/P10/J22/", name)[0]
x = get_coordinates(directory, name)[0]
#y = get_coordinates("/storage2/labusr/20210402_TetraCU428/P10/J22/", name)[1]
y = get_coordinates(directory, name)[1]
plt.scatter(x, y, marker='.', c = 'b')

if (ground_truth is not None):
    x_g = get_coordinates("", ground_truth)[0]
    y_g = get_coordinates("", ground_truth)[1]
    plt.scatter(x,y, marker=".", c = 'r')

    truth = pd.concat([x_g,y_g], axis = 1)
    print(truth)
    print(truth.shape)
    prediction = pd.concat([x,y], axis = 1)

    truth = truth.to_numpy()
    prediction = prediction.to_numpy()
    overlapped_points = overlapped_points(truth, prediction, int(args.radius))
    overlapped_np = np.asarray(overlapped_points)
    print(overlapped_points)
    print(overlapped_np)

    plt.scatter(overlapped_np[:,0], overlapped_np[:,1], c= 'o')



plt.gca().set_aspect('equal', adjustable='box')
#plt.gca().invert_yaxis()

plt.show()
if (args.s is not None):
    plt.savefig(os.path.join(args.s, os.path.basename(name).replace(".mrc", ""), format = "png"))
plt.close()
