import os
import sys
import argparse
import multiprocessing as mp

import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

sys.path.append(".")

import matplotlib.pyplot as plt
import pandas as pd

from utils.parsers import *
from utils.filament_fit import *

sys.path.append(".")

parser = argparse.ArgumentParser(
    description="Traces coordinates along filaments, spaced equidistantly after every given pixel value")

parser.add_argument("filament_PATH", help="location of filament files")

parser.add_argument("-t", "--threshold", help="threshold for particle extraction", type=float)

parser.add_argument("save_PATH", help="save location for fitted filament plots")

parser.add_argument("spacing", help="distance between neighbouring particles", type=float)

parser.add_argument("-eps", "--eps", nargs='?', const=10, help="The maximum distance between two " +
                                                               "samples for one to be considered " +
                                                               "as in the neighborhood of the other. "
                    , type=float)
parser.add_argument("-im", "--image", nargs="?", const=0,
                    help="if specified with 1, will save an image for the coordiantes as png as well",
                    type=bool)
parser.add_argument("-min_samples", "--min_samples", nargs="?", const=5,
                    help="The number of samples (or total weight) in a neighborhood for a point to be considered as a core point. This includes the point itself."
                    , type=float)
parser.add_argument("-box", "--box_size", nargs="?", const=100, help="box size of the selected particles", type=int)
parser.add_argument("-min_part", "--min_part", nargs="?", const=10,
                    help="the minimum number of particles in a cluster/filament", type=int)
parser.add_argument("-processors", "--processors", nargs="?", const= 1, help="Number of processors to use", type=int)

args = parser.parse_args()

box_size = args.box_size

min_part = args.min_part

# convert to numpy
file_library = None
if args.threshold is not None:
    file_library = parse_helix_coordinates(args.filament_PATH, threshold=args.threshold)
    print("args.threshold is provided")
else:
    file_library = parse_helix_coordinates(args.filament_PATH)


def process_file(file):
    print("Writing filament coordiantes for " + file)
    img = file_library[file]
    plt.scatter(img[0], img[1], marker=".")
    plt.close()
    list_of_clusters = DBSCAN_fit(img, eps=args.eps, min_samples=args.min_samples)

    df = pd.DataFrame()

    fig1 = plt.figure(1)

    helix_id = 1
    for cluster in list_of_clusters:

        try:
            poly_o = ransac_fit.polyfit(cluster, 2, 1, disable_linear=False, directory_mode=False)
            arclength_o = ransac_fit.arclength(poly_o)
            x = ransac_fit.spacing(arclength_o, args.spacing)

            y = poly_o["model"].predict(x)
            x = [(item[0]) for item in x]

            # swap the x and y predicted if they were intially swapped by polyfit
            if (poly_o["swapped"] == True):
                tmp = x
                x = y
                y = tmp

            if len(x) < min_part:
                continue

            # image option
            ax1 = None
            if (args.image == 1):
                ax1 = fig1.gca()
                ax1.plot(x, y, color="purple")
                ax1.scatter(cluster[:, 0], cluster[:, 1])

            df2 = pd.DataFrame({'x': x, 'y': y, "box_size": box_size, "box_size_2": box_size, "helix_id": helix_id})
            df = df.append(df2)
            helix_id += 1
        except ValueError as e:
            continue
    # image option
    if (args.image == 1):
        ax1.set_title(file)
        fig1.savefig(args.save_PATH + "/" + file.replace(".txt", ".png"))
    df.to_csv(args.save_PATH + "/" + file.replace(".txt", ".box"), sep="\t", index=False, header=False)
    return 99


if __name__ == "__main__":

    pool = mp.Pool(args.processors)

    results = pool.map(process_file, [file for file in file_library])

    pool.close()

    exit(100)
