
from __future__ import division

import csv
import math
import logging
from datetime import datetime
from os.path import exists

import pygame
import numpy as np
from pykinect import nui
from skimage.measure import label, regionprops

from evaluate import points_per_label, centroid_from_points

# ------------------------------------------------------------------------------
# constants & config

logging.basicConfig(level=logging.DEBUG)

UINT16_MIN = 0
UINT16_MAX = 65535

KINECT_DEPTH_INT = (0, 8000)
KINECT_CANVAS_SIZE = (320, 240)
KINECT_FRAME_LIMIT = 2
KINECT_PIXEL_DEPTH = 16

PYGAME_FONT_SIZE = 16
PYGAME_FONT_COLOR = (255, 255, 255)

KEY_HANDSIGN_MAP = {}
KEY_HANDSIGN_MAP[pygame.K_p] = "pierre"
KEY_HANDSIGN_MAP[pygame.K_c] = "ciseaux"
KEY_HANDSIGN_MAP[pygame.K_f] = "feuille"

# ------------------------------------------------------------------------------
# features vector helpers

def point_from_frame (frame):
    frame = label(frame)
    regions = regionprops(frame)

    if regions:
        props = max(regions, key=lambda region: region.area)

        return np.array([
            # cirularity
            4 * math.pi * props.area / props.perimeter ** 2 if props.perimeter else -1,
            # ellipticity
            props.minor_axis_length / props.major_axis_length if props.major_axis_length else -1,
            # convexivity
            props.convex_area / props.area if props.area else -1
        ])

def classify_point (point, centroids):
    min_dist = float("inf")
    min_label = "unknown"
    
    # find centroid with minimum distance
    for label, centroid in centroids.iteritems():
        dist = np.linalg.norm(point-centroid)
        if dist < min_dist:
            min_dist = dist
            min_label = label

    return min_label 

# ------------------------------------------------------------------------------
# frame processing middleware

class HandSignFilter (object):

    def __init__(self, canvas, interval, centroids):
        self.font = pygame.font.SysFont('Arial', PYGAME_FONT_SIZE)
        self.point = None
        self.frame = None
        self.canvas = canvas
        self.inverse_shape = canvas.get_size()[::-1]
        self.interval = interval
        self.centroids = centroids

    def on_depth_frame (self, depth_frame):
        if self.canvas.get_locked():
            return

        # convert kinect frame to numpy ndarray
        frame = np.frombuffer(depth_frame.image.bits, dtype=np.uint16)

        # inverse shape, then swap axes
        frame.shape = self.inverse_shape
        frame = np.swapaxes(frame, 0, 1)

        # filter by distance
        lower, upper = self.interval
        predicate = (lower < frame) & (frame < upper)
        frame = np.where(predicate, UINT16_MAX, UINT16_MIN)

        # set and draw the frame
        self.frame = frame
        pygame.pixelcopy.array_to_surface(self.canvas, frame)

        # set and draw point and its category
        self.point = point_from_frame(self.frame)
        if self.point is not None:
            label = classify_point(self.point, self.centroids)
            text = self.font.render(label, True, PYGAME_FONT_COLOR)
            self.canvas.blit(text, (PYGAME_FONT_SIZE, PYGAME_FONT_SIZE))

        # update pygame surface
        pygame.display.update()

    def on_depth_frame_simple (self, depth_frame):
        depth_frame.image.copy_bits(self.canvas._pixels_address)
        pygame.display.update()

# ------------------------------------------------------------------------------
# frame processing middleware

def main(train_dump):

    # read training data for estimates
    if exists(train_dump):
        logging.info('using centroids from : %s' % train_dump)
        centroids = { label: centroid_from_points(points) \
            for label, points in points_per_label(train_dump).iteritems() }
    else:
        logging.info('no training data available')
        centroids = {}
        
    # create pygame canvas
    logging.debug('initializing pygame')
    pygame.init()
    pygame.display.set_caption("Pierre-Feuille-Ciseaux")
    canvas = pygame.display.set_mode(KINECT_CANVAS_SIZE, 0, KINECT_PIXEL_DEPTH)

    # create frame handler
    hsf = HandSignFilter(canvas, KINECT_DEPTH_INT, centroids)

    # record handsigns to
    recordpath = datetime.now().strftime("assets/samples/%Y-%m-%d-%H-%M-%S.samples.csv")
    logging.info('samples path : %s' % recordpath)

    # open ressources
    with open(recordpath, "wb") as record, nui.Runtime() as kinect:

        writer = csv.writer(record, delimiter=';')

        logging.debug('initializing kinect stream')
        kinect.depth_frame_ready += hsf.on_depth_frame
        kinect.depth_stream.open(
            nui.ImageStreamType.Depth,
            KINECT_FRAME_LIMIT,
            nui.ImageResolution.Resolution320x240,
            nui.ImageType.Depth
            )

        # game event loop
        while True:
            event = pygame.event.wait()

            if event.type == pygame.KEYUP and event.key in KEY_HANDSIGN_MAP:
                if hsf.point is None:
                    continue
                
                row = [KEY_HANDSIGN_MAP[event.key]]
                row.extend(["%.6f" % feature for feature in hsf.point])

                writer.writerow(row)
                logging.info('recorded data point: %s' % ";".join(row))

            elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE or \
                 event.type == pygame.QUIT:
                logging.debug('exiting pygame')
                pygame.quit()
                break

if __name__ == "__main__":
    main('assets/samples.csv')