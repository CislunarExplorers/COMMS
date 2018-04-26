import cv2
import cv2.cv as cv
import numpy as np
import time
import argparse

from vision_util import Circle, FilteredImage, show_image

MAX_DISPLAY_SIZE = 1024



# TODO: function to perform RANSAC circle detection based off of an initial guess of circle size.


def hough_detect_circle(img):
    img = cv2.medianBlur(img,5)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # circles = cv2.HoughCircles(img,cv.CV_HOUGH_GRADIENT, 1, 10,
    #                              param1=40,param2=70,minRadius=10, maxRadius=200)
    print 'starting Hough'
    circles = cv2.HoughCircles(img,cv.CV_HOUGH_GRADIENT, 1, 10, param1=30,param2=80,minRadius=200, maxRadius=700)
    print 'Hough done'
    if circles == None:
        print("Hough failed!")
        return None
    else:
        circle = circles[0,0]
        yc = int(round(circle[0]))
        xc = int(round(circle[1]))
        r = int(round(circle[2]))
        return Circle(xc, yc, r)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input", metavar='i', type=str, help="filename of the input image")
    #parser.add_argument("output", metavar='o', type=str, help="output filename", default="")
    args = parser.parse_args()
    img = cv2.imread(args.input, cv2.IMREAD_COLOR)
    start_time = time.time()
    circle = hough_detect_circle(img)
    runtime = time.time() - start_time
    circle.draw(img)
    print("%----------- HOUGH RESULTS -----------%")
    print("Runtime is %s seconds" % runtime)
    show_image(img, title="Hough circle result")
    cv2.waitKey(0)