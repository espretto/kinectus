

from sys import exit
from os import listdir, makedirs
from os.path import join, dirname, realpath, splitext, basename, exists, isfile
from enum import Enum

import math
from skimage import io
from skimage.color import rgb2gray
from skimage.measure import label, regionprops

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pprint import pprint as pp

# ------------------------------------------------------------------------------
# setup
BASE_DIR = dirname(realpath(__file__))

def absolute (relative):
    return join(BASE_DIR, relative)

def dirabs (dir):
    return [join(dir, path) for path in listdir(dir)]

SOURCE_DIR = absolute('img/source')
TRAIN_DIR = absolute('img/source/train')

if not exists(TRAIN_DIR):
    makedirs(TRAIN_DIR)

RED = 0; GREEN = 1; BLUE = 2

# ------------------------------------------------------------------------------
# core

def show_image (img):
    io.imshow(img)
    io.show()

def extract_channel (img, channel):
    return img[:, :, channel]

def crop_margin (img, margin):
    height, width, depth = img.shape
    return img[margin:width-margin, margin:height-margin]

def prepare (img):
    img = crop_margin(img, 42)
    img = extract_channel(img, BLUE)
    img = rgb2gray(img)
    img = img > 250 # binarize with custom threshold
    return img

def describe (img):
    img_labeled = label(img)
    props = regionprops(img_labeled)[0]

    return {
        'circularity': 4 * math.pi * props.area / props.perimeter ** 2,
        'ellipticity': props.minor_axis_length / props.major_axis_length,
        'convexivity': props.convex_area / props.area
        }

def classify (desc):
    path = desc['path']

    if 'Ciseaux' in path:
        return 'red'
    elif 'Feuille' in path:
        return 'blue'
    else:
        return 'green'

# ------------------------------------------------------------------------------
# run

if __name__ == '__main__':

    paths = dirabs(SOURCE_DIR)
    results = []

    for path in filter(isfile, paths):
        img = io.imread(path)
        img = prepare(img)
        result = describe(img)
        result['path'] = path
        results.append(result)

    # plot the surface
    plt3d = plt.figure().gca(projection='3d')

    # Ensure that the next plot doesn't overwrite the first plot
    ax = plt.gca()
    ax.hold(True)

    for res in results:
        color = classify(res)
        ax.scatter(res['circularity'], res['ellipticity'], res['convexivity'], color=color)

    plt.show()
    pp(results)


# ------------------------------------------------------------------------------
# archive

def insertext (basename, ext):
    return ext.join(splitext(basename))

def crop_images(source, target, bbox):
    from PIL import Image
    paths = dirabs(source)

    for path in paths:
        img = Image.open(path)
        bboxed = img.crop(bbox)
        img.close()
        filename = insertext(basename(path), '.slice')
        bboxed.save(join(target, filename))
