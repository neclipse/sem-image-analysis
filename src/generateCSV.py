"""CSV Metafile Generator

This script generates a CSV datafile from loaded TXT metafiles

Instructions:
Copy this script and place it in the folder containing the metadata TXT files.
Open up Command Prompt or Powershell and navigate to thee folder containing
the metadata TXT files and the copy of this script. Execute the script by
running python generateCSV.py and a CSV file will be produced according to the
time and date.
"""
import os
import csv
import time
import tkinter
from tkinter.filedialog import askdirectory
tkinter.Tk().withdraw()
metaDir = askdirectory(title='Select Folder')
# currentDir = os.getcwd() # Possible alternative to run from command line
fileList = os.listdir(metaDir)

fieldnames = []

# Create new CSV file:
csvName = time.strftime("%Y%m%d-%H%M%S") + '.csv'
csvPath = os.path.join(metaDir, csvName)
listOfMetadata = []

for filename in fileList:
    if not filename.endswith(".txt"):
        continue
    filepath = os.path.join(metaDir, filename)

    # Open file and begin looping through
    metadataFile = open(filepath)
    metadata = {}
    for line in metadataFile:
        line = line.strip()
        if len(line) < 1:
            continue
        if "," not in line:
            print("Formatting error, no comma found")
            print(filepath)
            continue
        split = line.split(",", 1)
        label = split[0].strip()
        data = split[1].strip().replace(",", "#")
        if label not in fieldnames:
            fieldnames.append(label)
        metadata[label] = data
    if len(metadata) > 0:
        listOfMetadata.append(metadata)

with open(csvPath, mode='w') as dataFile:
    writer = csv.DictWriter(dataFile, fieldnames=fieldnames)
    writer.writeheader()
    for metadata in listOfMetadata:
        writer.writerow(metadata)