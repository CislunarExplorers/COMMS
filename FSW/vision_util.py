
import numpy as np
import cv2
import argparse
from least_square_circle import leastsq_circle
from random import sample
from scipy.spatial.distance import cdist
import time


MAX_DISPLAY_SIZE = 1024


class Circle(object):

    def __init__(self, x, y, r, inliers=[]):
        self.x = int(round(x))
        self.y = int(round(y))
        self.r = int(round(r))
        self._inliers = inliers
        self._num_inliers = len(inliers)

    @property
    def inliers(self):
        return self._inliers

    @inliers.setter
    def inliers(self, inliers):
        self._inliers = inliers
        self._num_inliers = len(inliers)

    @property
    def num_inliers(self):
        return self._num_inliers
    
    def draw(self, img, color=(0,0,255)):
        cv2.circle(img, (self.y, self.x), self.r, color, 2)

    def __str__(self):
        return ("Circle with center (x={}, y={}) and radius r={}. Circle has {} RANSAC inlier points.".format(self.x, self.y, self.r, self.num_inliers))
    

"""
Filtering strategy:

Earth shows up as mostly blue (sky, oceans) and white (clouds), with a little green and brown (land).
Moon shows up as just a dull grey.
"""

class FilteredImage(object):

    def __init__(self, hsv_img):
        self.earth_img = None
        self.moon_img = None
        self.filter(img)

    def filter(self, hsv_img):
        """
        Given an image, which may contain the Moon, the Earth, both, or none:

        1.) Filter out the pixels that are blue or white - these correspond to the Earth.
            Create a color image of just the Earth pixels and save it in self.earth_img
        2.) From all other pixels in the image, filter out non-black pixels - these correspond to the Moon.
            Create a color image of just the Moon pixels and save it in self.moon_img
        """

        # TODO: Improve earth and moon color bounds
        earth_low = np.array([90, 0, 0])
        earth_hi = np.array([130, 255, 255])
        earth_low2 = np.array([0, 0, 100])
        #earth_low2 = np.array([0, 0, 255])
        earth_hi2 = np.array([180, 255, 255])
        moon_low = np.array([0, 0, 0])
        moon_hi = np.array([0, 0, 0])
        earth_blue_filter = cv2.inRange(hsv_img, earth_low, earth_hi)
        earth_white_filter = cv2.inRange(hsv_img, earth_low2, earth_hi2)
        earth_filtered = np.bitwise_or(earth_blue_filter, earth_white_filter)
        moon_filtered = cv2.inRange(hsv_img, moon_low, moon_hi)

        self.earth_img = earth_filtered
        self.moon_img = moon_filtered
        if SHOW_FILTERED_IMAGES:
            show_image(earth_blue_filter, title='Earth  blue filter')
            show_image(earth_white_filter, title='Earth white filter')
            show_image(self.earth_img, title='Earth filter')
            #show_image(self.moon_img, title='Moon filter')
            cv2.waitKey(0)

def show_image(img, title="Image"):
    s= img.shape
    rows = s[0]
    cols = s[1]
    if rows > MAX_DISPLAY_SIZE or cols > MAX_DISPLAY_SIZE:
        if rows > cols:
            new_cols = int(round(cols * float(MAX_DISPLAY_SIZE) / rows))
            img = cv2.resize(img, dsize=(new_cols, MAX_DISPLAY_SIZE))
        else:
            new_rows = int(round(rows * float(MAX_DISPLAY_SIZE) / cols))
            img = cv2.resize(img, dsize=(MAX_DISPLAY_SIZE, new_rows))
    cv2.imshow(title, img)