
from __future__ import division

import csv
import numpy as np

if __name__ == "__main__":

    centroids = {}
    centroids_count = {}
    centroids_total = {}
    
    with open('assets/records/2018-02-07-15-59-54.record.csv', 'rb') as record:
        reader = csv.reader(record, delimiter=';')
        
        for row in reader:
            group = row[0]

            if group in centroids_total:
                centroids_total[group] += np.array(map(float, row[1:]))
                centroids_count[group] += 1
            else:
                centroids_total[group] = np.array(map(float, row[1:]))
                centroids_count[group] = 1

    for group, total in centroids_total.iteritems():
        centroids[group] = total / centroids_count[group]

    for group, centroid in centroids.iteritems():
        print(group, str(centroid))