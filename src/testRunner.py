import os
import contourDetection


def mainLoop():
    directory = r'dataset\sample'
    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.endswith(".tif"):
                contourDetection.detectContours(filepath)


def main():
    filepath = r'dataset\sample\SS 316 P&C_#1_002.tif'
    contourDetection.detectContours(filepath, alg="MED", debug=False)


if __name__ == "__main__":
    main()