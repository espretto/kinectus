
from __future__ import division

from os import listdir, makedirs
from os.path import join, dirname, realpath, splitext, basename, exists, isfile

# ------------------------------------------------------------------------------
# config & constants

BASE_DIR = dirname(realpath(__file__))
RED = 0; GREEN = 1; BLUE = 2

# ------------------------------------------------------------------------------
# helper methods

def absolute (relative):
    return join(BASE_DIR, relative)

def dirabs (dir):
    return [join(dir, path) for path in listdir(dir)]

def insertext (basename, ext):
    return ext.join(splitext(basename))

def extract_channel (img, channel):
    return img[:, :, channel]

def crop_margin (img, margin):
    height, width, depth = img.shape
    return img[margin:width-margin, margin:height-margin]

def prepare (img):
    from skimage.color import rgb2gray

    img = crop_margin(img, 42)
    img = extract_channel(img, BLUE)
    img = rgb2gray(img)
    img = img > 250 # binarize with custom threshold
    return img

def describe (img):
    import math
    from skimage.measure import label, regionprops
    
    img_labeled = label(img)
    props = regionprops(img_labeled)[0]

    return {
        circularity: 4 * math.pi * props.area / props.perimeter ** 2,
        ellipticity: props.minor_axis_length / props.major_axis_length,
        convexivity: props.convex_area / props.area
        }

def crop_image(source, bbox):
    from PIL import Image

    with Image.open(path) as img:
        target = insertext(basename(path), '.slice')
        img.crop(bbox).save(target)
