from skimage.morphology import skeletonize
from skimage import data
import matplotlib.pyplot as plt
from skimage.util import invert

#input: outputs of clustering algorithms
def parse_clusters(cluster_outpus)

    coordinates = list_of_clusters[0]
    for i in range(1,len(list_of_clusters)):
        coordinates = np.concatenate((coordinates, list_of_clusters[i]))
    plt.scatter(coordinates[:,0], coordinates[:,1])
    print(coordinates)

    npmap = np.zeros((np.max(coordinates[:,0]+1), np.max(coordinates[:,1]+1)))

    x = np.arange(0, np.max(coordinates[:,1]+1))
    y = np.arange(0, np.max(coordinates[:,0]+1))

    print(npmap.shape)
    r = 15

    for i in range(len(coordinates)):
        npmap[coordinates[i][0]][coordinates[i][1]]=1
        cx = coordinates[i][0]
        cy = coordinates[i][1]
        
        mask = (x[np.newaxis,:]-cx)**2 + (y[:,np.newaxis]-cy)**2 < r**2
        npmap[mask] = 1

def skeletonize(image):

    image = npmap

    # perform skeletonization
    skeleton = skeletonize(image)

def cross_removal(skeleton, radius = 20):
    cross_points = []
    for i in range(skeleton.shape[0]):
        for j in range(skeleton.shape[1]):
            if (skeleton[i,j]):
                num_neibours = 0
                if (i != 0 and j != 0 and i != skeleton.shape[0]-1 and j != skeleton.shape[1]):
                    subarray = skeleton[i-1:i+2, j-1:j+2]
                    if (np.count_nonzero(subarray) >= 4):
                        cross_points.append((i,j))

    all_points = tuple(zip(*np.where(skeleton == True)))


    import numpy as np
    import scipy.spatial as spatial
    points = np.array(all_points)
    print(points)

    plt.scatter(points[:,0], points[:,1])
    plt.show()

    point_tree = spatial.cKDTree(points)

    for cross_point in np.asarray(cross_points):
        list_of_points = (point_tree.data[point_tree.query_ball_point(cross_point,radius)])
        for point in list_of_points:
            print(point)
            skeleton[int(point[0])][int(point[1])] = 0
    
    return skeleton

def get_points(skeleton):
    all_points = tuple(zip(*np.where(skeleton > 0)))
    return all_points

