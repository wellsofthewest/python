#Christian Wells
#IMAPS 2013
#
#Name: Append Features to Master GDB
#
#Purpose: This tool uses the arcpy and os module to add each feature from
#a completed map to the Master GDB.

import arcpy, os

finalPath = r"M:\dep\GIS_Project\PITT\Completed Maps"
MOA = r"M:\gis\Master_Geodatabases\Master_Collection_Geodatabase.gdb\PITT\Coal_Seam_Elevations"

quadList = []
for i in os.listdir(finalPath):
    if i != "Thumbs.db":
        path = os.path.join(finalPath, i, i + "_GIS_Map_Template.gdb", "Coal_Seam_Elevations")
        quadList.append(path)
        print i
arcpy.Append_management(quadList, MOA)
