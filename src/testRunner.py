import os
import numpy as np
import cv2
import contourDetection
import cornerDetection
import matplotlib.pyplot as plt

def mainLoop():
    directory = r'dataset\sample'
    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.endswith(".tif"):
                contourDetection.detectContours(filepath)


def main():
    # Do some preprocessing
    filepath = r'dataset\sample\SS 316 P&C_#1_002.tif'
    img = cv2.imread(filepath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
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

    image = cv2.bitwise_and(img, img, mask=mask)
    # cv2.drawContours(image, validContours, -1, (0, 255, 0), 1)
    # Convert numpy array mask into an openCV image
    # mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # Take the mask, blur it, and apply corner detection
    maskBlur = cv2.GaussianBlur(mask, (9,9), 0)
    corners = cornerDetection.detectHarrisCornerGeneric(maskBlur, debug=False)

    # Also get new contours while you're at it
    cv2.imshow("MASK", mask)
    cv2.waitKey(0)
    maskContours, maskHierarchy = contourDetection.detectContours(mask, debug=False)

    cv2.drawContours(image, maskContours, -1, (255, 0, 0), 1)
    print(type(mask))
    print(type(image))
    # image[corners > 0.01 * corners.max()] = [0, 0, 255]
    image[corners > 0.1 * corners.max()] = [0, 0, 255]
    print("Corners extracted")

    # Convert mask to color
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    #cv2.drawContours(mask, maskContours, -1, (0, 255, 0), -1)
    #cv2.drawContours(image, validContours, -1, (0, 255, 0), -1)

    cv2.imshow("ORIGINAL", img)
    cv2.imshow("MASK", mask)
    cv2.imshow("IMAGE", image)
    if cv2.waitKey(0) and 0xff == 27:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()