#-------------------------------------------------------------------------------
# Name:        Iterate Subfolders and Create Map Document
#
# Purpose:
# This script iterates through images within a workspace, finds images with
# the extentsion .sid and adds them into a new directory, creates a map based on
# the subfolder name, and then adds the image to the map document. This
# can be used for an organization that utilizes a one-up directory system or
# has many subfolders that contain images and need a map created for them.
#
# Author:      Christian Wells
#-------------------------------------------------------------------------------

import arcpy, os

#Workspace folder location and template MXD file
folderPath = r"C:\ImageFolders"
templateMap = r"C:\Template.mxd"

#Iterate through images in workspace
for i in os.listdir(folderPath):
    #Find image extension
    value =  i[-3:]
    if value =="sid":
        #Create paths to create directory, MXD, and move raster
        mapDir = i[:5]
        sidPath = os.path.join(folderPath, i)
        mapDirPath = os.path.join(folderPath, str(mapDir))
        sidNewPath = os.path.join(folderPath, str(mapDir), i)
        mapPath = os.path.join(mapDirPath, mapDir + ".mxd")
        rasterLayer = mapDir

        #Create directory, MXD, and move raster
        try:
            #Create Directory
            os.mkdir(os.path.join(folderPath, str(mapDir)))
            #Copy Raster to new location
            arcpy.Copy_management(sidPath, sidNewPath)
            print "     Directory and SID created"
            #Save a copy of the template map to the new directory
            rasterMD = arcpy.mapping.MapDocument(templateMap)
            rasterMD.saveACopy(mapPath)
            print "     Creating MXD"
            md = arcpy.mapping.MapDocument(mapPath)
            df = arcpy.mapping.ListDataFrames(md)[0]
            #Add raster image to the MXD
            result = arcpy.MakeRasterLayer_management(sidNewPath, rasterLayer)
            layer = result.getOutput(0)
            arcpy.mapping.AddLayer(df, layer, 'AUTO_ARRANGE')
            #Save map
            md.save()
            print "     Map Complete"
        except:
            print "Directory already exists for : " + mapDir