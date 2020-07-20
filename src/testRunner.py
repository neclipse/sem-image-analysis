import os
import numpy as np
import cv2
import contourDetection
import cornerDetection
import matplotlib.pyplot as plt


def main():
    """
    directory = r'dataset\sample'
    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.endswith(".tif"):
                contourDetection.detectContours(filepath)
    """


def processing():
    # Do some preprocessing
    # filepath = r'dataset\sample\SS 316 P&C_#1_002.tif'
    filepath = r'dataset\sample\800_020.tif'
    img = cv2.imread(filepath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #blur = cv2.GaussianBlur(gray, (5, 5), 0)
    blur = cv2.medianBlur(gray, 10)
    input = blur
    canny = contourDetection.generateCanny(input, alg="MED", debug=False)
    # dilate then erode the canny to close edges
    kernel = np.ones((3, 3), np.uint8)      # MODIFY THIS AS NECESSARY
    closing = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel)
    #dilation = cv2.dilate(canny, kernel, iterations=1)
    contours, hierarchy = contourDetection.detectContours(closing, debug=False)

    # Create the mask based on the detected contours
    image = None
    mask = np.ones(img.shape[:2], dtype="uint8") * 255
    validContours = []  # List of valid contours
    print("Looping through contours")
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        area = cv2.contourArea(contour)
        if area > 25:
            validContours.append(contour)
            cv2.drawContours(mask, [contour], -1, (0, 255, 0), -1)

        # Uncomment below lines to show mask and image as its being drawn (unstable)
        # cv2.imshow('mask', mask)
        # cv2.imshow('image', image)
        # cv2.waitKey(1)

    print("Contour analysis complete.")
    """
    maskBGR = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    _, alpha = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)
    b, g, r = cv2.split(maskBGR)
    rgba = [b, g, r, 0.5]
    maskBGR = cv2.merge(rgba, 4)
    image = cv2.addWeighted(img, 0.5, maskBGR, 0.5, 0.0)
    """

    image = cv2.bitwise_and(img, img, mask=mask)
    # cv2.drawContours(image, validContours, -1, (0, 255, 0), 1)
    # Convert numpy array mask into an openCV image
    # mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # Take the mask, blur it, and apply corner detection
    maskBlur = cv2.GaussianBlur(mask, (9,9), 0)
    # corners = cornerDetection.detectHarrisCornerGeneric(mask, debug=False)
    corners = cornerDetection.goodFeatureShiTomasi(mask)
    print(type(corners))

    # Also get new contours while you're at it
    #cv2.imshow("MASK", mask)
    #cv2.waitKey(0)
    maskContours, maskHierarchy = contourDetection.detectContours(mask, debug=False)

    #cv2.drawContours(image, maskContours, -1, (255, 0, 0), 1)
    print(type(mask))
    print(type(image))
    # image[corners > 0.01 * corners.max()] = [0, 0, 255]
    # threshold = 0.1 * corners.max()
    # image[corners > threshold] = [0, 0, 255]
    print("Corners Detected: {}".format(corners.size))

    # Convert mask to color
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    for i in corners:
        x, y = i.ravel()
        cv2.circle(img, (x, y), 3, 255, -1)

    #cv2.drawContours(mask, maskContours, -1, (0, 255, 0), -1)
    #cv2.drawContours(image, validContours, -1, (0, 255, 0), -1)

    # NUMBER OF CONNECTED COMPONEENTS:


    cv2.imshow("ORIGINAL", img)
    cv2.imshow("MASK", mask)
    cv2.imshow("IMAGE", image)
    if cv2.waitKey(0) and 0xff == 27:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()