import cv2
import numpy as np


def detectHarrisCornerGeneric(input, debug=False):
    corners = cv2.cornerHarris(input, 4, 3, 0.04)   # TODO: TWEAK WITH IMPROVED PARAMETERS
    # corners = cv2.dilate(corners, None)         # make corners more clear
    return corners

def detectHarrisCornerAccurate(input):
    # TODO: AFTER STUDING REFERENCE DOCS, IMPLEMENT PIXEL-ACCURATE CORNER DETECTION
    pass