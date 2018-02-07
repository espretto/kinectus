
from __future__ import division
from pykinect import nui
from skimage.measure import label, regionprops
from datetime import datetime
import math
import numpy as np
import pygame

# ------------------------------------------------------------------------------
# constants & config

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

class DataPoint (object):

    def __init__ (self, region_props):
        self.circularity = 4 * math.pi * region_props.area / region_props.perimeter ** 2 if region_props.perimeter else -1
        self.ellipticity = region_props.minor_axis_length / region_props.major_axis_length if region_props.major_axis_length else -1
        self.convexivity = region_props.convex_area / region_props.area if region_props.area else -1

    def to_csv_line (self, sign):
        return "%s;%f;%f;%f\n" % (
            sign,
            self.circularity,
            self.ellipticity,
            self.convexivity
            )

    @staticmethod
    def from_frame (frame):
        frame = label(frame)
        regions = regionprops(frame)

        if regions:
            region_props = max(regions, key=lambda region: region.area)
            return DataPoint(region_props)

# ------------------------------------------------------------------------------
# frame processing middleware

class HandSignFilter (object):

    def __init__(self, canvas, interval):
        self.frame = None
        self.canvas = canvas
        self.interval = interval

    def on_depth_frame (self, depth_frame):
        # convert kinect frame to numpy ndarray
        frame = np.frombuffer(depth_frame.image.bits, dtype=np.uint16)

        # inverse shape, then swap axes
        frame.shape = self.canvas.get_size()[::-1]
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
    pygame.init()
    pygame.display.set_caption("Pierre-Feuille-Ciseaux")
    canvas = pygame.display.set_mode(KINECT_CANVAS_SIZE, 0, KINECT_PIXEL_DEPTH)

    # create frame handler
    hsf = HandSignFilter(canvas, KINECT_DEPTH_INT)

    # record handsigns to..
    recordpath = datetime.now().strftime("assets/records/record-%Y-%m-%d-%H-%M-%S.csv")

    with open(recordpath, "a") as recorder, nui.Runtime() as kinect:
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
                data_point = DataPoint.from_frame(hsf.frame)
                
                if not data_point:
                    continue

                csv_line = data_point.to_csv_line(handsign)
                recorder.write(csv_line)
                print('stored data point: %s' % csv_line)

            elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE or \
                 event.type == pygame.QUIT:
                pygame.quit()
                break

if __name__ == "__main__":
    main()