import cv2
import numpy as np


def detectHarrisCornerGeneric(input, debug=False):
    corners = cv2.cornerHarris(input, blockSize=10, ksize=11, k=0.04)   # TODO: TWEAK WITH IMPROVED PARAMETERS
    # corners = cv2.dilate(corners, None)         # make corners more clear
    return corners

def detectHarrisCornerAccurate(input):
    # TODO: AFTER STUDING REFERENCE DOCS, IMPLEMENT PIXEL-ACCURATE CORNER DETECTION
    pass


def goodFeatureShiTomasi(input):
    corners = cv2.goodFeaturesToTrack(input, maxCorners=100000, qualityLevel=0.01, minDistance=10,
                                      blockSize=3, mask=None, useHarrisDetector=False)
    corners = np.int0(corners)
    return corners


def goodFeatureHarrisCorner(input):
    corners = cv2.goodFeaturesToTrack(input, maxCorners=100000, qualityLevel=0.01, minDistance=10,
                                      blockSize=3, mask=None, useHarrisDetector=True)
    corners = np.int0(corners)
    return corners