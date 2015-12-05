#Christian Wells
#IMAPS 2013
#
#Name: Get Spatial Reference for SID
#
#Purpose: This tool uses the arcpy and os module to list MrSID images
#spatial reference system. If the system is not PA South or North. The
#name of the reference will be printed.

import arcpy, os


finalPath = r"M:\dep\GIS_Project\PITT\ToDigitize"
finalList = []



for i in os.listdir(finalPath):
    sidPath = os.path.join(finalPath, i)
    for g in os.listdir(sidPath):
        value = g[-3:]
        if value =="sid":
            try:
                sidRef = arcpy.Describe(os.path.join(sidPath, g)).spatialReference.Name
                if sidRef == "NAD_1983_StatePlane_Pennsylvania_South_FIPS_3702_Feet":
                    a = "c"
                elif sidRef == "NAD_1983_StatePlane_Pennsylvania_North_FIPS_3701_Feet":
                    b = "b"
                else:
                    print i + ":  " + sidRef

            except:
                print i + " Code Error"
