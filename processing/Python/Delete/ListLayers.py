import arcpy, os
from arcpy import mapping as m

map = r"C:\temp\Japan.mxd"

mxd = m.MapDocument(map)

for df in m.ListDataFrames(mxd):
    print '\nDataframe: {}'.format(df.name)
    for lyr in m.ListLayers(mxd, '', df):
        if lyr.supports('DATASOURCE'):
            print '\t{0:.<50} {1}'.format(lyr.name, lyr.dataSource)