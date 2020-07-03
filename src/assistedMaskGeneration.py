"""User-assisted Mask Generation

"""
import os
import tkinter
import cv2
from tkinter.filedialog import askdirectory
import numpy as np
import contourDetection

imgDir = askdirectory(title='Select Folder')
fileList = os.listdir(imgDir)
for filename in fileList:
    continue