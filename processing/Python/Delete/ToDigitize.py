#Christian Wells
#IMAPS 2013
#
#Name: Move folder from QC to Digitize
#
#Purpose: This tool uses the arcpy and os module to copy directories
#from QC to digitize and populate with a GDB for digitizing. The GDB
#is given the ID Sort of the map.

import arcpy
import os


workpath = arcpy.GetParameterAsText(0)
workpathList = workpath.split(";")
newWorkpath = arcpy.GetParameterAsText(1)
fileGDB = r"M:\gis\Geodatabases\_GIS_Map_Template.gdb"

for path in workpathList:
    try:
        arcpy.AddMessage("Processing: " + path)
        folderName = os.path.basename(path)
        gdbName = os.path.basename(fileGDB)
        arcpy.Copy_management(str(path), os.path.join(newWorkpath, folderName))
        arcpy.AddMessage("  Copy of " + path + " successful")
        arcpy.AddMessage("  Deleting: " + path)
        arcpy.Delete_management(str(path))
        arcpy.AddMessage("  Removal of " + path + " successful")
        arcpy.AddMessage("  Creating file geodatabse for map " + folderName)
        arcpy.Copy_management(fileGDB, os.path.join(newWorkpath, folderName, str(folderName + gdbName)))
        arcpy.AddMessage("  File GDB creation for map " + folderName + " successful")
    except:
        arcpy.AddMessage("Copy of " + folderName + " did not succeed!")



del path

