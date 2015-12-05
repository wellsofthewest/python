import os, sys, time, arcpy

minx = sys.argv[1]
miny = sys.argv[2]
maxx = sys.argv[3]
maxy = sys.argv[4]
FEMA_ID = sys.argv[5]

path = os.path.join(r"C:\TEMP", FEMA_ID + ".pdf")
mxd = arcpy.mapping.MapDocument(r"C:\Demos\PYSQL\BASE.mxd")
data_frame = arcpy.mapping.ListDataFrames(mxd)[0]
extent = arcpy.Extent(float(minx),float(miny),float(maxx),float(maxy))
data_frame.extent = extent
arcpy.mapping.ExportToPDF(mxd,path)


