import argparse
import os

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import glob
import os
from PIL import Image
from topaz.utils.data.loader import load_image
from matplotlib.patches import Circle
from gooey import Gooey

@Gooey
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("micrographs",
                        help="The specified path for the micrograph you want to visualize, including its name")
    parser.add_argument("topaz_predictions",
                        help="The specified path to the topaz coordinate file you have generated from training")
    parser.add_argument("--r", '--radius', help="The radius of particles", const=15)
    parser.add_argument("train_test_split_files", help="path to the train test split files generated from topaz")

    args = parser.parse_args()

    predicted_particles = pd.read_csv(args.topaz_predictions, sep='\t')

    _ = plt.hist(predicted_particles.score, bins=50)
    plt.xlabel('Predicted score (predicted log-likelihood ratio)')
    plt.ylabel('Number of particles')
    plt.show()

    proba = 1.0 / (1.0 + np.exp(-predicted_particles.score))
    _ = plt.hist(proba, bins=50)
    plt.xlabel('Predicted probability of y=1')
    plt.ylabel('Number of particles')
    plt.show()

    threshold = input("Enter a threshold value you would like to test")
    print("Number of particles above threshold:" + str(np.sum(predicted_particles.score >= float(threshold))))

    ## load the micrographs for visualization
    micrographs = {}
    for path in glob.glob(args.micrographs):
        im = np.array(load_image(path), copy=False)
        name, _ = os.path.splitext(os.path.basename(path))
        micrographs[name] = im

    ## load the train/test split so we can look at results on test set only!
    images_train = pd.read_csv(os.path.join(args.train_test_split, "image_list_train.txt"), sep='\t')
    images_train = set(images_train.image_name)

    images_test = pd.read_csv(os.path.join(args.train_test_split, "image_list_test.txt"), sep='\t')
    images_test = set(images_test.image_name)
    image_names = list(images_test)  # micrograph names for the test set

    proceed = True
    while(proceed):
        name = input("Name of the file you would like to visualize:")
        radius = input("Radius of particle size you would like to visualize")
        lowerbound = input("Lower bound of the threshold")
        upperbound = input("Upper bound of the threshold")
        visualizer(micrographs, predicted_particles, name, radius, lowerbound, upperbound)

        response = input("Visualize more micrographs? (Y/N)")
        if response == "Y" or response == "y" or response == "yes" or response == "Yes":
            continue
        else:
            proceed = False


def visualizer(micrographs, predicted_particles, name, radius = 15, lowerbound=-1000, upperbound=1000):
    name = "Map9_00041_3-2"
    print(name)
    im = micrographs[name]
    raw_particles = predicted_particles.loc[predicted_particles['image_name'] == name]

    # visualize predicted particles with log-likelihood ratio >= 0 (p >= 0.5)

    threshold = -5
    particles = raw_particles.loc[raw_particles['score'] >= lowerbound].loc[raw_particles['score'] <= upperbound]

    _, ax = plt.subplots(figsize=(16, 16))
    ax.imshow(im, cmap='Greys_r', vmin=-3.5, vmax=3.5, interpolation='bilinear')

    radius = radius

    threshold_steps = 25

    colours = matplotlib.cm.get_cmap('viridis', threshold_steps)

    threshold_vals = np.linspace(raw_particles["score"].min(), raw_particles["score"].max(), threshold_steps)

    # Normalizde the threshold_vals

    i = 0
    c_map = {}
    for col in colours.colors:
        c_map[threshold_vals[i]] = col
        i = i + 1

    # plot the predicted particles in blue
    for x, y, score in zip(particles.x_coord, particles.y_coord, particles.score):
        # if (score <= 1.5): continue;
        index = find_nearest(threshold_vals, score)
        c = Circle((x, y), radius, fill=False, color=c_map[index])
        ax.add_patch(c)

    plt.show()
    plt.close()


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

if __name__ == "__main__":
    main()
