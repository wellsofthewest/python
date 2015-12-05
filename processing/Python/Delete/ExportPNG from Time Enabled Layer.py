#-------------------------------------------------------------------------------
# Name:        ExportPNG from Time Enabled Layer
# Purpose:
#
# Author:      LuisV
#
# Created:     14/01/2014
# Copyright:   (c) luis0000 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
import os

mxd = arcpy.mapping.MapDocument(r"C:\Pytest\test.mxd")
df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
df.time.currentTime = df.time.startTime

while df.time.currentTime <= df.time.endTime:
    # An example str(newTime) would be: "2008-12-29 02:19:59"
    # The following line splits the string at the space and takes the first
    # item in the resulting string.
    fileName = str(df.time.currentTime) + ".png"
    fileName = fileName.replace(":", "-")
    arcpy.mapping.ExportToPNG(mxd, os.path.join(r"C:\Pytest", fileName), df,
                          df_export_width=1600,
                          df_export_height=1200,
                          world_file=True)
    df.time.currentTime = df.time.currentTime + df.time.timeStepInterval
del mxd