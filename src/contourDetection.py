import cv2
import os


def detectContours(filepath):
    org = cv2.imread(filepath)
    img = cv2.imread(filepath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 1)
    #cv2.imshow("blur", blur)

    ret, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_OTSU)
    cv2.imshow("thresh", thresh)

    canny = cv2.Canny(thresh, 75, 200)
    cv2.imshow('canny', canny)

    contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contour_list = []
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        # area = cv2.contourArea(contour)
        # if 5000 < area < 15000:
        contour_list.append(contour)

    msg = "Total holes: {}".format(len(approx) // 2)
    cv2.putText(img, msg, (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2, cv2.LINE_AA)

    cv2.drawContours(org, contour_list, -1, (0, 255, 0), 1)
    cv2.imshow('Objects Detected', org)

    cv2.waitKey(0)





