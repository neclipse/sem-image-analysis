"""User-assisted Mask Generation

"""
import os
from tkinter import *
import cv2
from tkinter.filedialog import askdirectory
import numpy as np
import contourDetection


def main():
    imgDir = askdirectory(title='Select Folder')
    fileList = os.listdir(imgDir)
    for filename in fileList:
        window = Tk()
        window.title("Make necessary Modifications")
        continue


if __name__ == "__main__":
    main()