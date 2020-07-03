"""Training Data Mask Generator

This script automatically attmepts to generate a mask for training data based
on edge detection methods to be modified in external software.
"""
import os
import tkinter
import cv2
from tkinter.filedialog import askdirectory
import numpy as np
import contourDetection

tkinter.Tk().withdraw()
imgDir = askdirectory(title='Select Folder')
# currentDir = os.getcwd() # Possible alternative to run from command line
fileList = os.listdir(imgDir)
for filename in fileList:
    if not filename.endswith(".tif")\
            and not filename.endswith(".jpg") \
            and not filename.endswith(".png"):
        continue

    filepath = os.path.join(imgDir, filename)
    origImg = cv2.imread(filepath)
    height, width, channels = origImg.shape

    grayImg = cv2.cvtColor(origImg, cv2.COLOR_BGR2GRAY)
    # ROI = grayImg[0:int(height*.80), 0:width]
    blur = cv2.bilateralFilter(grayImg, d=29, sigmaColor=75, sigmaSpace=75)
    blur = cv2.medianBlur(blur, 5)
    ROI = blur[0:int(height*.80), 0:width]
    canny = contourDetection.generateCanny(blur, ROI=ROI, alg="SAM")

    kernel = np.ones((3, 3), np.uint8)

    closing = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel)
    contours, hierarchy = contourDetection.detectContours(closing)


    # Create the mask
    mask = np.ones(origImg.shape[:2], dtype="uint8") * 255
    validContours = []  # List of valid contours
    for contour in contours:
        approx = cv2.approxPolyDP(
            contour,
            0.01 * cv2.arcLength(contour, True),
            True
        )
        area = cv2.contourArea(contour)
        if area > 50:
            validContours.append(contour)
            cv2.drawContours(mask, [contour], -1, (0, 255, 0), -1)

    maskedImage = cv2.bitwise_and(origImg, origImg, mask=mask)
    maskFilename = os.path.splitext(filename)[0] + ".png"
    maskDir = os.path.join(imgDir, "segmentation")
    if not os.path.exists(maskDir):
        os.mkdir(maskDir)
    maskFilepath = os.path.join(maskDir, maskFilename)
    maskFilepath = os.path.normpath(maskFilepath)
    cv2.imwrite(maskFilepath, mask)

    cv2.imshow("ORIG", origImg)
    cv2.imshow("BLUR", blur)
    cv2.imshow("GRAY", grayImg)
    cv2.imshow("CANNY", canny)
    # cv2.imshow("CLOSING", closing)
    cv2.imshow("MASK", mask)
    cv2.waitKey()
    cv2.destroyAllWindows()

print("Done.")