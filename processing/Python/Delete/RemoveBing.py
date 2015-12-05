# ---------------------------------------------------------------
# Script: MXD broken link indicator & repair
#
# Date: February 11, 2014
#
# Description: The following script will go through a desired
# directory and determine which MXDs have broken data sources
# within the subfolders. In addition, it will change the
# broken data sources which were found.
#
# Note: The 'path' variable should be updated to match the
# directory you are interested in searching with in and the
# 'newDB' variable should be adjusted to the location of the
# sde connection file that should be used to resource the data.
# ** This script is designed to only have to resource data that
# is from the same data source.
# ---------------------------------------------------------------

# Import Modules
import arcpy, os

# Declare variables
path = arcpy.GetParameterAsText(0)
newDB = arcpy.GetParameterAsText(1)

# Uncomment the following, and comment out the varaibles above if interested in runnning the tool through Python
'''
path = r"C:\Users\just7460\Desktop\Documents\Incidents\1237657"
newDB = r"C:\Users\just7460\Desktop\Documents\Incidents\1237657\sde@steven.sde"
'''

for root, dirs, files in os.walk(path):
    print "\n" + root
    arcpy.AddMessage("\n" + root)
    for fileName in os.listdir(root):
        fullPath = os.path.join(root, fileName)
        if os.path.isfile(fullPath):
            basename, extension = os.path.splitext(fullPath)
            if extension == ".mxd":
                mxd = arcpy.mapping.MapDocument(fullPath)
                print "\n\tMXD: " + mxd.filePath
                arcpy.AddMessage("\n\tMXD: " + mxd.filePath)
                for df in arcpy.mapping.ListDataFrames(mxd, ""):
                    print "\t\tData Frame: " + df.name
                    arcpy.AddMessage("\t\tData Frame: " + df.name)
                    # Remove Bing Maps if uncommented
                    
                    for layer in arcpy.mapping.ListLayers(mxd, "*Bing*", df):
                        arcpy.mapping.RemoveLayer(df, layer)
                        print "\t\t\tBing layer: " + layer.name + " removed"
                        arcpy.AddMessage("\t\t\tBing layer: " + layer.name + " removed")
                    
                    # Find the broken links in the Map Document
                    brknList = arcpy.mapping.ListBrokenDataSources(mxd)
                    if len(brknList) > 0:
                        print "\tMXD: " + fileName
                        arcpy.AddMessage("\tMXD: " + fileName)
                        # Try to replace the broken data sources with the new SDE connection
                        for brknItem in brknList:
                            try:
                                oldDB = brknItem.workspacePath
                                brknItem.findAndReplaceWorkspacePath(oldDB, newDB, True)
                                print "\t\t\t\tWorkspace successfully replaced"
                                arcpy.AddMessage ("\t\t\t\tWorkspace successfully replaced")
                                mxd.save()
                            except:
                                print "\t\t\t\tERROR: Unable to validate new workspace path for " + brknItem.name
                                arcpy.AddMessage("\t\t\t\tERROR: Unable to validate new workspace path for " + brknItem.name)

                    

