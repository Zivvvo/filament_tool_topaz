import matplotlib.pyplot as plt
import numpy as np
import sklearn
import pandas as pd
import os
import sys
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
sys.path.append(".")
from . import ransac_fit

#convert coodinate files generated by any EMAN picking programs(ie. e2helixboxer.py) into coordinate files supported by topaz
def parse_EMAN_coordinates(path_to_EMAN, path_to_topaz):
    EMAN_files = os.listdir(path_to_EMAN)
    EMAN_files = [x for x in EMAN_files if ".txt" in x]
    #some special cases

    t = open(path_to_topaz+"/particle_coords.txt", "w")

    t.write("image_name\tx_coord\ty_coord\n")
    for file in EMAN_files:
        ofile = file.replace(".txt", "")

        print(ofile)

        f = open(path_to_EMAN + "/" + file, "r")
        for i in range(6):
            f.readline()
        for line in f:
            if (not ("#helix: " in line)):
                nums = line.split("\t")
                nums = [float(x) for x in nums]

                nfile = file.replace(".txt", "")
                t.write(nfile + "\t" + str(int(nums[0])) + "\t" + str(int(nums[1])) + "\n")


#convert coordinate files generated by the topaz program into coordinate files supported by filament mode
def parse_topaz_coordinates(path_to_topaz, path_to_helix):
    f = open(path_to_topaz, "r")
    f.readline()  # skip one line
    o = None

    current_title = ""

    for x in f:
        line = x.split("\t")
        if line[0] != current_title:
            current_title = line[0]
            o = open(path_to_helix + "/" + line[0] + ".txt", "w")

            o.write("x_coord\ty_coord\tscore\n")
            o.write(line[1] + "\t" + line[2] + "\t" + line[3])
        else:
            o.write(line[1] + "\t" + line[2] + "\t" + line[3])
    return 1

#input: a directory containing input coordinate files generated by parse_topaz_coordinates
#returns an dictionary of coordinates whose elements are in the following format:
#       "file_name": x_coords(np array) y_coords(np array)
def parse_helix_coordinates(path, threshold=-2.5):
    #parse each file
    file_library = {}
    threshold_score = -2.5

    for file in os.listdir(path)[1:]:
        try:
            df = pd.read_csv(os.path.join(path,file), sep="\t")
            df = df.drop(df[df.score<threshold_score].index)
            x = df["x_coord"].to_numpy()
            y = df["y_coord"].to_numpy()
            tup = (x,y)
            file_library.update({file: tup})
        except AttributeError:
            #if an input file did not satisfy requirements
            continue

    return file_library
