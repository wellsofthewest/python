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

workpath = r"M:\dep\GIS_Project\GeorefSID"
sidpath = r"M:\web\SID"
namelist=[]


for i in range(20970, 21036):
    os.mkdir(os.path.join(workpath, str(i)))
    sid = os.path.join(sidpath, str(i) + ".sid")
    print sid
    outsid = os.path.join(workpath, str(i), str(i) + ".sid")
    print outsid
    arcpy.Copy_management(sid, outsid)
    print i
