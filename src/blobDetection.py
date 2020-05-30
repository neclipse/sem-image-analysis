import cv2
import numpy as np
import os


def detectBlobs(filename):
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    detector = cv2.SimpleBlobDetector_create()
    keypoints = detector.detect(img)

    imgWithKeypoints = cv2.drawKeypoints(
        img,
        keypoints,
        np.array([]),
        (0, 0, 255),
        cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
    )

    cv2.imshow("Keypoints", imgWithKeypoints)
    cv2.waitKey(0)
