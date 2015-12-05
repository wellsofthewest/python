#Christian Wells
#IMAPS 2013
#
#Name: Create Directories and MXD for MrSID images
#
#Purpose: This tool uses the arcpy and os module to list MrSID images in one
#root folders. Once the images are listed a directory is created using the base
#name of the image. After the directory is created, the image is added to its proper
#directory. Lastly, a map for the ID Sort is created and the MrSID file is added to is.

import arcpy, os


georefPath = r"M:\dep\GIS_Project\PITT\Georef\ToGeoref"
georefMap = r"M:\dep\Manuals and Procedures\Georef.mxd"

for i in os.listdir(georefPath):
    value =  i[-3:]
    if value =="sid":
        mapDir = i[:5]
        sidPath = os.path.join(georefPath, i)
        mapDirPath = os.path.join(georefPath, str(mapDir))
        sidNewPath = os.path.join(georefPath, str(mapDir), i)
        mapPath = os.path.join(mapDirPath, mapDir + ".mxd")
        rasterLayer = mapDir
        try:
            os.mkdir(os.path.join(georefPath, str(mapDir)))
            arcpy.Copy_management(sidPath, sidNewPath)
            print "     Directory and SID created"
            georefMD = arcpy.mapping.MapDocument(georefMap)
            georefMD.saveACopy(mapPath)
            print "     Creating MXD"
            md = arcpy.mapping.MapDocument(mapPath)
            df = arcpy.mapping.ListDataFrames(md)[0]
            result = arcpy.MakeRasterLayer_management(sidNewPath, rasterLayer)
            layer = result.getOutput(0)
            arcpy.mapping.AddLayer(df, layer, 'AUTO_ARRANGE')
            md.save()
            print "     Map Complete"
        except:
            print "Directory already exists for : " + mapDir

