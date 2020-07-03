import cv2
import numpy as np
import imutils

_OTSU = "OTSU"
_MED = "MED"
_SAM = "SAM"
options = [_OTSU, _MED, _SAM]
_SIGMA = 0.33


def generateCanny(input, ROI, alg="MED", debug=False):
    assert alg in options
    canny = None
    if alg == _OTSU:
        upper, thresh = cv2.threshold(ROI, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        lower = 0.5 * upper
        canny = cv2.Canny(input, lower, upper)
        if debug:
            cv2.imshow("thresh", thresh)
    elif alg == _MED:
        v = np.median(ROI)
        lower = int(max(0, (1.0 - _SIGMA) * v))
        upper = int(min(255, (1.0 + _SIGMA) * v))
        canny = cv2.Canny(input, lower, upper)
    elif alg == _SAM:
        upper = 255 * 0.75
        lower = 255 * 0.50
        canny = cv2.Canny(input, lower, upper)

    if debug:
        cv2.imshow("CANNY", canny)
        if cv2.waitKey(0) and 0xff == 27:
            cv2.destroyAllWindows()

    return canny


def detectContours(input, debug=False):
    contours, hierarchy = cv2.findContours(input, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    return contours, hierarchy

