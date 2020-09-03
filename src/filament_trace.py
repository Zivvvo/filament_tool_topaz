import os
import sys
import argparse
sys.path.append(".")

import matplotlib.pyplot as plt
import pandas as pd

from utils.parsers import *
from utils.filament_fit import *

sys.path.append(".")

parser = argparse.ArgumentParser(description="Traces coordinates along filaments, spaced equidistantly after every given pixel value")

parser.add_argument("filament_PATH", help="location of filament files")

parser.add_argument("-t", "--threshold", help="threshold for particle extraction", type=float)

parser.add_argument("save_PATH", help="save location for fitted filament plots")

parser.add_argument("spacing", help="distance between neighbouring particles", type= float)

args = parser.parse_args()

#convert to numpy
file_library = None
if args.threshold is not None:
    file_library = parse_helix_coordinates(args.filament_PATH, threshold = args.threshold)
    print("args.threshold is provided")
else:
    file_library = parse_helix_coordinates(args.filament_PATH)


for file in file_library:
    print(file)
    img = file_library[file]
    plt.scatter(img[0], img[1], marker=".")
    plt.close()
    list_of_clusters = DBSCAN_fit(img, eps=15, min_samples=5)

    df = pd.DataFrame()

    fig1 = plt.figure(1)

    for cluster in list_of_clusters:
        try:
            poly_o = ransac_fit.polyfit(cluster, 2, 1, disable_linear=True, directory_mode=False)
            arclength_o = ransac_fit.arclength(poly_o)
            x = ransac_fit.spacing(arclength_o, args.spacing)

            y = poly_o["model"].predict(x)

            #swap the x and y predicted if they were intially swapped by polyfit
            if (poly_o["swapped"] == True):
                tmp = x
                x = y
                y = tmp

            ax1 = fig1.gca()
            ax1.plot(x, y, color="purple")
            ax1.scatter(cluster[:, 0], cluster[:, 1])

            df2 = pd.DataFrame({'x': x, 'y': y})
            df = df.append(df2)
        except ValueError as e:
            print(e)
            continue
    ax1.set_title(file)
    fig1.savefig(args.save_PATH+"/"+file.replace(".txt", ".png"))
    df.to_csv(args.save_PATH+"/"+file.replace(".txt", ".csv"))


