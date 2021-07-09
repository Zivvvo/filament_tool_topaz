import os
import sys
import argparse
import multiprocessing as mp
from gooey import Gooey
import warnings
import matplotlib.pyplot as plt
import pandas as pd
from functools import partial
import numpy as np

sys.path.append(".")
from utils.parsers import *
from utils.filament_fit import *

warnings.filterwarnings("ignore", category=DeprecationWarning)

@Gooey

def main():
    sys.path.append(".")

    parser = argparse.ArgumentParser(
        description="Traces coordinates along filaments, spaced equidistantly after every given pixel value")

    parser.add_argument("filament_PATH", help="location of filament files")

    parser.add_argument("-t", "--threshold", nargs= '?', default= -3, help="threshold for particle extraction", type=float)

    parser.add_argument("save_PATH", help="save location for fitted filament plots")

    parser.add_argument("spacing", help="distance between neighbouring particles", type=float)

    parser.add_argument("-eps", "--eps", nargs='?', default=10, help="The maximum distance between two " +
                                                                   "samples for one to be considered " +
                                                                   "as in the neighborhood of the other. "
                        , type=float)
    parser.add_argument("-im", "--image", nargs="?", default=0,
                        help="if specified with 1, will save an image for the coordiantes as png as well",
                        type=bool)
    parser.add_argument("-min_samples", "--min_samples", nargs="?", default=5,
                        help="The number of samples (or total weight) in a neighborhood for a point to be considered as a core point. This includes the point itself."
                        , type=float)
    parser.add_argument("-box", "--box_size", nargs="?", default=100, help="box size of the selected particles", type=int)
    parser.add_argument("-min_part", "--min_part", nargs="?", default=10,
                        help="the minimum number of particles in a cluster/filament", type=int)
    parser.add_argument("-processors", "--processors", nargs="?", default= 2, help="Number of processors to use", type=int)

    parser.add_argument("-to_segment", "--segment", nargs="?", default = 0, help="Segment long clusters into subclusters", type =bool)

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

    pool = mp.Pool(args.processors)

    func = partial(process_file, file_library, args)

    results = pool.map(func, [file for file in file_library])

    pool.close()

    pool.join()

    exit(100)


def process_file(file_library, args, file):
    print("Writing filament coordinates for " + file)
    img = file_library[file]
    plt.scatter(img[0], img[1], marker=".")
    plt.close()
    try:
        list_of_clusters = DBSCAN_fit(img, eps=args.eps, min_samples=args.min_samples)
    except ValueError as e:
        print(e)
        print("no clusters found, continuing to next file")
        return -100

    df = pd.DataFrame()

    fig1 = plt.figure(1)

    helix_id = 1

    ax1 = None


    if (args.segment == 1):
        def range_of_vals(x, axis=0):
            return np.max(x, axis=axis) - np.min(x, axis=axis)

        def max_var_axis(cluster):
            arr = np.array(cluster)
            if (range_of_vals(arr[:, 0]) >= range_of_vals(arr[:, 1])):
                return 0
            else:
                return 1

        def sort(cluster, axis=0):
            # axis = 0 --> x axis
            if axis == 0:
                return cluster[cluster[:, 0].argsort()]
            else:
                return cluster[cluster[:, 1].argsort()]

        def average_length(lst):
            lengths = [len(i) for i in lst]
            return 0 if len(lengths) == 0 else (float(sum(lengths)) / len(lengths))

        sorted_list_of_cluster = sorted(list_of_clusters, key=len, reverse=True)
        clusters_to_fit = []
        avg_len = average_length(sorted_list_of_cluster)

        for i in range(len(sorted_list_of_cluster)):
            if len(sorted_list_of_cluster[i]) > 1.5 * avg_len:
                clst = sorted_list_of_cluster[i]

                clst = sort(clst, axis=max_var_axis(clst))

                clst_half1 = clst[:int(len(clst) / 2)]
                clst_half2 = clst[int(len(clst) / 2):]

                clusters_to_fit.append(clst_half1)
                clusters_to_fit.append(clst_half2)
            else:
                clusters_to_fit.append(sorted_list_of_cluster[i])
        list_of_clusters = clusters_to_fit

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

            if len(x) < args.min_part:
                continue

            # image option
            ax1 = None
            if (args.image == 1):
                ax1 = fig1.gca()
                ax1.plot(x, y, color="purple")
                ax1.scatter(cluster[:, 0], cluster[:, 1])

            df2 = pd.DataFrame({'x': x, 'y': y, "box_size": args.box_size, "box_size_2": args.box_size, "helix_id": helix_id})
            df = df.append(df2)
            helix_id += 1
        except ValueError as e:
            print(e)
            continue

    # image option
    if (args.image == 1 and ax1 != None):
        ax1.set_title(file)
        fig1.savefig(args.save_PATH + "/" + file.replace(".txt", ".png"))
    df.to_csv(args.save_PATH + "/" + file.replace(".txt", ".box"), sep="\t", index=False, header=False)
    return 99


if __name__ == "__main__":
    main()
