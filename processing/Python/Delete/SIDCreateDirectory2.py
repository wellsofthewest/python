#Christian Wells
#IMAPS 2013
#
#Name: Create Directories for MrSID images
#
#Purpose: This tool uses the arcpy and os module to list MrSID images in one
#root folders. Once the images are listed a directory is created using the base
#name of the image. After the directory is created, the image is added to its proper
#directory.

import arcpy, os


finalPath = r"M:\dep\GIS_Project\PITT\Georef"
for i in os.listdir(finalPath):
    value =  i[-3:]
    if value =="sid":
        mapDir = i[:5]
        try:
            os.mkdir(os.path.join(finalPath, str(mapDir)))
            arcpy.Copy_management(os.path.join(finalPath, i), os.path.join(finalPath, str(mapDir), i))
        except:
            print "Directory already exists for : " + mapDir
        
        
        
        
