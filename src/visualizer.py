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

parser = argparse.ArgumentParser()

parser.add_argument('filename', help = "filename")
parser.add_argument('binfactor', default = 1, type = int)
parser.add_argument('directory', default = "", help = "directory to the box file")


parser.add_argument('--prefix', default = "", help = "prefix of the filename")
parser.add_argument('--suffix', default = "", help = "suffix of the filename")
parser.add_argument('--ground_truth', help = "path to the box_file that acts as a reference")
parser.add_argument('--s' , default = None, help = "if set, will save output image to designated path")

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

ground_truth = os.path.splitext(args.ground_truth)
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


Nx, Ny = im.shape
binx = round(Nx/binfactor)
biny = round(Ny/binfactor)
im_bin = rebin(im, (binx,biny))

plt.imshow(im_bin, cmap= "gray")



#x = get_coordinates("/storage2/labusr/20210402_TetraCU428/P10/J22/", name)[0]
x = get_coordinates(directory, name)[0]
#y = get_coordinates("/storage2/labusr/20210402_TetraCU428/P10/J22/", name)[1]
y = get_coordinates(directory, name)[1]
plt.scatter(x, y, marker='.', c = '#1f77b4')

if (ground_truth is not None):
    x_g = get_coordinates("", ground_truth)[0]
    y_g = get_coordinates("", ground_truth)[1]
    plt.scatter(x,y, marker=".", c = '#7f7f7f')

plt.gca().set_aspect('equal', adjustable='box')
#plt.gca().invert_yaxis()

plt.show()
if (args.s is not None):
    plt.savefig(os.path.join(args.s, os.path.basename(name).replace(".mrc", ""), format = "png"))
plt.close()
