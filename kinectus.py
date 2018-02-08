
from __future__ import division

import csv
import math
import logging
from datetime import datetime

import pygame
import numpy as np
from pykinect import nui
from skimage.measure import label, regionprops

# ------------------------------------------------------------------------------
# constants & config

logging.basicConfig(level=logging.DEBUG)

UINT16_MIN = 0
UINT16_MAX = 65535

KINECT_DEPTH_INT = (0, 8000)
KINECT_CANVAS_SIZE = (320, 240)
KINECT_FRAME_LIMIT = 2
KINECT_PIXEL_DEPTH = 16

KEY_HANDSIGN_MAP = {}
KEY_HANDSIGN_MAP[pygame.K_p] = "pierre"
KEY_HANDSIGN_MAP[pygame.K_c] = "ciseaux"
KEY_HANDSIGN_MAP[pygame.K_f] = "feuille"

# ------------------------------------------------------------------------------
# data point / feature vector

class Features (object):

    CIRCULARITY = 0
    ELLIPTICITY = 1
    CONVEXIVITY = 2

    @staticmethod
    def from_frame (frame):
        frame = label(frame)
        regions = regionprops(frame)

        if regions:
            props = max(regions, key=lambda region: region.area)

            return np.array([
                4 * math.pi * props.area / props.perimeter ** 2 if props.perimeter else -1,
                props.minor_axis_length / props.major_axis_length if props.major_axis_length else -1,
                props.convex_area / props.area if props.area else -1
            ])

# ------------------------------------------------------------------------------
# frame processing middleware

class HandSignFilter (object):

    def __init__(self, canvas, interval):
        self.frame = None
        self.canvas = canvas
        self.inverse_shape = canvas.get_size()[::-1]
        self.interval = interval

    def on_depth_frame (self, depth_frame):
        # convert kinect frame to numpy ndarray
        frame = np.frombuffer(depth_frame.image.bits, dtype=np.uint16)

        # inverse shape, then swap axes
        frame.shape = self.inverse_shape
        frame = np.swapaxes(frame, 0, 1)

        # filter by distance
        lower, upper = self.interval
        predicate = (lower < frame) & (frame < upper)
        frame = np.where(predicate, UINT16_MAX, UINT16_MIN)

        # set last frame
        self.frame = frame

        # update canvas
        pygame.pixelcopy.array_to_surface(self.canvas, frame)
        pygame.display.update()

    def on_depth_frame_simple (self, depth_frame):
        depth_frame.image.copy_bits(self.canvas._pixels_address)
        pygame.display.update()

# ------------------------------------------------------------------------------
# frame processing middleware

def main():
    
    # create pygame canvas
    logging.debug('initializing pygame')
    pygame.init()
    pygame.display.set_caption("Pierre-Feuille-Ciseaux")
    canvas = pygame.display.set_mode(KINECT_CANVAS_SIZE, 0, KINECT_PIXEL_DEPTH)

    # create frame handler
    hsf = HandSignFilter(canvas, KINECT_DEPTH_INT)

    # record handsigns to..
    recordpath = datetime.now().strftime("assets/records/%Y-%m-%d-%H-%M-%S.record.csv")
    logging.info('records path : %s' % recordpath)

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

        while True:
            event = pygame.event.wait()

            if event.type == pygame.KEYUP and event.key in KEY_HANDSIGN_MAP:
                handsign = KEY_HANDSIGN_MAP[event.key]
                features = Features.from_frame(hsf.frame)
                
                if features is None:
                    continue

                row = [handsign]
                row.extend(["%.6f" % feature for feature in features])

                writer.writerow(row)
                logging.info('recorded data point: %s' % ";".join(row))

            elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE or \
                 event.type == pygame.QUIT:
                logging.debug('exiting pygame')
                pygame.quit()
                break

if __name__ == "__main__":
    main()