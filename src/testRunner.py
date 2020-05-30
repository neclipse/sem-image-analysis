import blobDetection
import os
import contourDetection


def main():
    directory = r'dataset\sample'
    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.endswith(".tif"):
                contourDetection.detectContours(filepath)


if __name__ == "__main__":
    main()