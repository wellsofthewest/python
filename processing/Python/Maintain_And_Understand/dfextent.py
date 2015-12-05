import arcpy

mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]
XM = 0
Xm = 0
YM = 0
Ym = 0
cnt = 0 
for layer in arcpy.mapping.ListLayers(mxd, "", df):
    ext = layer.getExtent("FALSE")
    extXM = ext.XMax
    extXm = ext.XMin
    extYM = ext.YMax
    extYm = ext.YMin
    while cnt == 0:
        XM = extXM
        Xm = extXm
        YM = extYM
        Ym = extYm
        cnt += 1        
    if extXM > XM:
        XM = extXM
    if extXm < Xm:
        Xm = extXm
    if extYM > YM:
        YM = extYM
    if extYm < Ym:
        Ym = extYm
newExtent = df.extent
newExtent.XMin, newExtent.YMin = Xm, Ym
newExtent.XMax, newExtent.YMax = XM, YM
df.extent = newExtent


