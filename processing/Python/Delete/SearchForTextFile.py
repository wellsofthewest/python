#Christian Wells
#IMAPS 2013
#
#Name: Search for Text File
#
#Purpose: This tool uses the arcpy and os module to list directories
#and search for a .txt file extension. If the file does not exist, it
#will be printed.

import os

finalPath = r"M:\dep\GIS_Project\PITT\ToDigitize"
finalList = []
folderList = []


for i in os.listdir(finalPath):
    sidPath = os.path.join(finalPath, i)
    folderList.append(i)
    for g in os.listdir(sidPath):
        value = g[-3:]
        if value =="txt":
            finalList.append(i)

for x in folderList:
    if x not in finalList:
        print x
