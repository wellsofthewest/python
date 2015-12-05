#Christian Wells
#IMAPS 2013
#
#Name: Add Features to a MXD
#
#Purpose: This tool uses the arcpy and os module to add each feature class from
#a list of directories by using os.listdir and adding the features to an already
#created MXD and then saving that map document.

import arcpy, os

mxd = arcpy.mapping.MapDocument(r"C:\Users\glds\Desktop\IndexMap.mxd")
df = arcpy.mapping.ListDataFrames(mxd,"Layers")[0]
finalPath = r"M:\dep\GIS_Project\R&P\DigInProgress"
for i in os.listdir(finalPath):
    try:
        print i
        tempLayer = i
        arcpy.MakeFeatureLayer_management(os.path.join(finalPath, i, i + "_GIS_Map_Template.gdb", "Digitized_Mined_Area"), tempLayer)
        addLayer = arcpy.mapping.Layer(tempLayer)
        arcpy.mapping.AddLayer(df, addLayer, "BOTTOM")
        print "     %s added to map" % i
    except:
        print i + " GDB needs renamed"
mxd.saveACopy(r"C:\Users\glds\Desktop\MOAMap.mxd")
del mxd, addLayer
