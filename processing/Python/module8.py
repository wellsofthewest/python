import arcpy, os
from arcpy import mapping as m


mxd = m.MapDocument(r'C:\temp\alex.mxd')
df = m.ListDataFrames(mxd)
qlyr = arcpy.MakeQueryLayer_management(r'Database Connections\Connection to CWELLS.sde', 'test2', 'select * from cities')
lyr = m.Layer('test2')
m.AddLayer(df[0], lyr)
mxd.save()