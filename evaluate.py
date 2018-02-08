
from __future__ import division

import csv
from itertools import groupby

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ------------------------------------------------------------------------------
# config & constants

LABEL_COLOR_MAP = {}
LABEL_COLOR_MAP['pierre'] = 'xkcd:pink'
LABEL_COLOR_MAP['feuille'] = 'xkcd:light green'
LABEL_COLOR_MAP['ciseaux'] = 'xkcd:light blue'

CENTROID_COLOR_MAP = {}
CENTROID_COLOR_MAP['pierre'] = 'xkcd:red'
CENTROID_COLOR_MAP['feuille'] = 'xkcd:green'
CENTROID_COLOR_MAP['ciseaux'] = 'xkcd:blue'

# ------------------------------------------------------------------------------
# helpers

def group_by (iterable, key):
    return groupby(sorted(iterable, key=key), key=key)

def get_label (row):
    return row[0]

def get_point (row):
    return np.array(map(float, row[1:]))

def centroid_from_points (points):
    return np.add.reduce(points) / len(points)

def points_per_label (recordpath):
    with open(recordpath, 'rb') as record:
        rows = csv.reader(record, delimiter=';')

        # read and group data points by label
        return { group: map(get_point, grouper) \
            for group, grouper in group_by(rows, key=get_label) }

# ------------------------------------------------------------------------------
# main

def main (recordpath):

    # create surface
    plt3d = plt.figure().gca(projection='3d')

    # ensure that the next plot doesn't overwrite the first plot (?)
    axis = plt.gca()
    axis.set_xlabel('circularity')
    axis.set_ylabel('ellipticity')
    axis.set_zlabel('convexivity')
    axis.hold(True)

    for label, points in points_per_label(recordpath).iteritems():
        
        # draw data points
        for point in points:
            axis.scatter(*point, color=LABEL_COLOR_MAP[label], s=2**4)

        # draw centroids (centers of mass)
        centroid = centroid_from_points(points)
        axis.scatter(*centroid, color=CENTROID_COLOR_MAP[label], s=2**6)

    plt.show()

# ------------------------------------------------------------------------------
# kickoff

if __name__ == '__main__':
    main('assets/records/samples.csv')

            

