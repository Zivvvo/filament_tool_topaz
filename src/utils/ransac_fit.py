import numpy as np
from sklearn import linear_model, datasets, metrics
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from matplotlib import pyplot as plt
import pandas as pd
import os


def polyfit(data, order, maxdistance, disable_linear=True, directory_mode=True):
    # loading and extracting columns of data for x and y
    # input data may be a string for directory, or a numpy array
    if (directory_mode):
        df = pd.read_csv(data, header=None)
        dfx = df[0].values
        dfy = df[1].values
    else: #numpy mode
        dfx = data[:, 0]
        dfy = data[:, 1]

    # if variance of x is low, swap x and y, to prevent a vertical line
    swapped = False
    if np.var(dfx) < np.var(dfy):
        tmp = dfx
        dfx = dfy
        dfy = tmp
        swapped = True

    x = np.reshape(dfx, (len(dfx), 1))

    y = np.reshape(dfy, (len(dfy),))

    # creation of the RANSACRegressor object
    ransac = make_pipeline(PolynomialFeatures(order), linear_model.RANSACRegressor(residual_threshold=maxdistance))

    ransac.fit(x, y)

    # creation of boolean mask arrays to indicate the (x,y) pairs that are inliers vs. outliers

    line_x = np.linspace(x.min(), x.max(), len(x))[:, np.newaxis]

    line_y_ransac = ransac.predict(line_x)

    # additional linear fit
    linear = linear_model.RANSACRegressor()
    linear.fit(x, y)

    inlier_mask = linear.inlier_mask_
    outlier_mask = np.logical_not(inlier_mask)

    line_y_linear = linear.predict(line_x)

    lw = 2

    #plt.scatter(x, y, color="red", marker='.')

    # select best fitted line using mean squared error

    MSE_regressor = metrics.mean_squared_error(dfy[:len(dfy)], line_y_ransac)
    MSE_linear = metrics.mean_squared_error(dfy[:len(dfy)], line_y_linear)

    '''print("MSE of the linear fit: " + str(MSE_linear))
    print("MSE of the polynomial fit: " + str(MSE_regressor))'''

    # determine the model to use based on lowest MSE

    chosen_model = None
    alternative_model = None
    chose = None
    if disable_linear == False:

        if (MSE_linear < MSE_regressor):
            chosen_model = linear
            chose = "linear"
            alternative_model = ransac
            #print("Linear model chosen")

            #plot_line(line_x, line_y_linear, 'LinearRegressor', lw, color="cornflowerblue")

        else:
            chosen_model = ransac
            chose = "ransac"
            alternative_model = linear
            #print("Polynomial model chosen")

            #plot_line(line_x, line_y_ransac, 'RANSACRegressor', lw, color="cornflowerblue")

    else:
        chosen_model = ransac
        alternative_model = linear
        #print("Polynomial model chosen")

        #plot_line(line_x, line_y_ransac, 'RANSACRegressor', lw, color="cornflowerblue")

    # information to be returned x_coords, y_coords(linear prediction), y_coords(polynomial prediction), chosen sklearn model, unchosen sklearn model
    cache = {"x": line_x, "yl": line_y_linear, "yr": line_y_ransac, "model": chosen_model,
             "alt_model": alternative_model, "MSE_linear": MSE_linear,"MSE_regressor": MSE_regressor, "swapped": swapped}

    return cache


def plot_line(x, y, label, lw, color='blue'):
    plt.plot(x, y, color=color, linewidth=lw,
             label=label)
    plt.legend(loc='lower right')
    plt.xlabel("Input")
    plt.ylabel("Response")

    xmin, xmax = plt.xlim()
    ymin, ymax = plt.ylim()

    if (xmax - xmin > ymax - ymin):
        plt.ylim((ymax + ymin) / 2 - (xmax - xmin) / 2, (ymax + ymin) / 2 + (xmax - xmin) / 2)
    else:
        plt.xlim((xmax + xmin) / 2 - (ymax - ymin) / 2, (xmax + xmin) / 2 + (ymax - ymin) / 2)
    print(plt.xlim())
    print(plt.ylim())

    plt.axis("equal")


def arclength(cache, linespace=5000):
    line_x = cache["x"]
    x_coords = np.linspace(line_x.min(), line_x.max(), linespace)[:, np.newaxis]
    y_coords = cache["model"].predict(x_coords)

    s_accumulative = 0.0
    s_list = []

    for i in range(len(x_coords) - 1):
        x_tmp = x_coords[i]
        y_tmp = y_coords[i]

        x_next = x_coords[i + 1]
        y_next = y_coords[i + 1]

        s_accumulative += np.sqrt(np.power((x_next - x_tmp), 2) + np.power((y_next - y_tmp), 2)).item()
        s_list.append(s_accumulative)

    return {"x": x_coords, "s(x)": s_list, "arclength": s_accumulative}


def spacing(cache, step_size):
    # based on the number of segments you want to divide the arc into, return the respective x coordinate at each segment

    l = np.arange(0, cache["arclength"], float(step_size))[:, np.newaxis]

    s = np.asarray(cache["s(x)"])

    x_locations = []
    for val in l:
        idx = np.abs(s - val).argmin()
        x_locations.append(cache["x"][idx])

    return x_locations


def process_data(directory, pixel_dist, disable_linear=True, indexi=0, indexj=10, parse_whole_dataset=False):
    file_list = os.listdir(directory)
    subset = [x for x in file_list if ".txt" in x]
    if (parse_whole_dataset == True):
        indexi = 0
        indexj = len(subset)

    for i in range(indexi, indexj):
        poly_o = polyfit(directory + "/" + subset[i], 2, 1, disable_linear=disable_linear)
        arclength_o = arclength(poly_o)
        output = spacing(arclength_o, pixel_dist)

        plt.scatter(output, poly_o["model"].predict(output))
        plt.savefig("test_data_plots/" + subset[i] + "_plot.png")
        plt.clf()

        unit_positions = pd.DataFrame({'x': output, 'y': poly_o["model"].predict(output)})
        unit_positions.to_csv(r"test_data_positions/" + subset[i] + "_unit_pos.txt", header=False, index=False)