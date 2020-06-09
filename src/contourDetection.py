import cv2
import numpy as np
import imutils

_OTSU = "OTSU"
_MED = "MED"
_SAM = "SAM"
options = [_OTSU, _MED, _SAM]
_SIGMA = 0.33


def detectContours(filepath, alg="MED", debug=False):
    assert alg in options

    img = cv2.imread(filepath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    process = blur
    canny = None

    if debug:
        cv2.imshow("gray", gray)
        cv2.imshow("blur", blur)

    if alg == _OTSU:
        upper, thresh = cv2.threshold(process, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        lower = 0.5 * upper
        canny = cv2.Canny(thresh, lower, upper)
        if debug:
            cv2.imshow("thresh", thresh)
    elif alg == _MED:
        v = np.median(process)
        lower = int(max(0, (1.0 - _SIGMA) * v))
        upper = int(min(255, (1.0 + _SIGMA) * v))
        canny = cv2.Canny(process, lower, upper)
    elif alg == _SAM:
        upper = 255
        lower = 255 * 0.33
        canny = cv2.Canny(process, lower, upper)


    if canny is None:
        print("Could not find canny.")
        return None

    kernel = np.ones((2, 2), np.uint8) # MODIFY THIS AS NECESSARY
    dilation = cv2.dilate(canny, kernel, iterations=1)
    cv2.imshow("canny", canny)
    cv2.imshow("dilation", dilation)

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    mask = np.ones(img.shape[:2], dtype="uint8") * 255

    posAreaContourList = []
    print("Looping through contours")
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        area = cv2.contourArea(contour)
        #print(area)
        if area > 20:
            posAreaContourList.append(contour)
            cv2.drawContours(mask, [contour], -1, (0, 255, 0), -1)
        #cv2.imshow('mask', mask)
        image = cv2.bitwise_and(img, img, mask=mask)
        #cv2.imshow('after', image)
        #cv2.waitKey(1)

    #cv2.drawContours(img, totalContourList, -1, (0, 0, 255), 1)
    cv2.drawContours(image, posAreaContourList, -1, (0, 255, 0), 1)
    cv2.imshow('after', image)
    cv2.waitKey(0)
    #cv2.drawContours(mask, contours, -1, (255, 255, 255), 1)

    #cv2.waitKey(0)

