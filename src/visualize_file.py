import argparse
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
from PIL import Image
from topaz.utils.data.loader import load_image
from matplotlib.patches import Circle

parser = argparse.ArgumentParser()

parser.add_argument("PATH", help="The specified path for the micrographs, including PATH")
parser.add_argument("PLOTS_PATH", help = "The specified path for the fitted plot coordinates")
parser.add_argument("--r", '--radius', help = "The radius of particles")

parser.add_argument("--s", "--SAVE_PATH", help="If specified, will save the file to the specified location")

args = parser.parse_args()

micrographs = {}
for path in glob.glob(args.PATH):
    im = np.array(load_image(path), copy=False)
    name,_ = os.path.splitext(os.path.basename(path))
    micrographs[name] = im

Continue = True
while (Continue):

    name = input("Enter the name of the microtubule file, do not include any file extensions (e.g. .mrc")

    print("visualization of filament fitting results for " + name)
    im = micrographs[name]

    # visualize predicted particles with log-likelihood ratio >= 0 (p >= 0.5)

    _,ax = plt.subplots(figsize=(16,16))
    ax.imshow(im, cmap='Greys_r', vmin=-3.5, vmax=3.5, interpolation='bilinear')

    radius = args.radius

    file_path = args.PLOTS_PATH + "/" + name + ".csv"
    df = pd.read_csv(file_path)

    # plot the predicted particles in blue
    for x,y in zip(df["x"],df["y"]):
        c = Circle((x,y),radius,fill=False,color='b')
        ax.add_patch(c)

    if (args.SAVE_PATH != None):
        ax.savefig("--SAVE_PATH")

    response = input("Continue? (y/n)")
    if (response == "n"):
        Continue = False


