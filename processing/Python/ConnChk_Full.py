import arcpy, os, math
from os import path as p

gn = arcpy.GetParameterAsText(0)
fc = arcpy.GetParameterAsText(1)
ext = arcpy.Describe(fc).extent


fd = p.dirname(gn)
gdb = p.dirname(fd)
gdbname = 'extFGDB.gdb'
extname = 'extGrids'
outdir = p.expanduser('~')
fldname = 'Verify_GN'

arcpy.env.outputCoordinateSystem = fc

if not p.exists(p.join(outdir, fldname)):
    os.mkdir(p.join(outdir, fldname))

outfc = p.join(outdir, fldname, gdbname, extname)

if not p.exists(p.join(outdir, fldname, gdbname)):
    arcpy.CreateFileGDB_management(p.join(outdir, fldname), gdbname)

xgrids = 5000
ygrids = 5000

if arcpy.Exists(outfc):
    arcpy.Delete_management(outfc)

stpnt = "{0} {1}".format(ext.XMin, ext.YMin)
ypnt = "{0} {1}".format(ext.XMin, ext.YMin+1)
endpnt = "{0} {1}".format(ext.XMax, ext.YMax)

arcpy.CreateFishnet_management(out_feature_class=outfc,
                               origin_coord=stpnt,
                               y_axis_coord=ypnt,
                               cell_width=ygrids,
                               cell_height=xgrids,
                               corner_coord=endpnt,
                               labels="NO_LABELS",
                               geometry_type="POLYGON")

lyrGrid = arcpy.MakeFeatureLayer_management(outfc, 'lyrGrid')
lyrFC = arcpy.MakeFeatureLayer_management(fc, 'lyrFC')

arcpy.SelectLayerByLocation_management(lyrGrid, 'INTERSECT', lyrFC)
arcpy.SelectLayerByAttribute_management(lyrGrid, 'SWITCH_SELECTION')
arcpy.DeleteFeatures_management(lyrGrid)

rows = arcpy.da.SearchCursor(outfc, ["OID@","SHAPE@"])

for row in rows:
    try:
        rowext = row[1].extent
        logfile = p.join(outdir, fldname, "Verify_Grid_{0}.txt".format(str(row[0])))
        arcpy.VerifyAndRepairGeometricNetworkConnectivity_management(gn, logfile, "VERIFY_AND_REPAIR", "EXHAUSTIVE_CHECK", rowext)
    except:
        arcpy.AddMessage('Errors in Grid OID: {0}'.format(str(row[0])))

sizes = []
grids = {}

##for f in os.listdir(path):
##    sizes.append(os.path.getsize(os.path.join(path, f)))
##    grids.update({'{}'.format(os.path.splitext(f[12:])[0]):os.path.getsize(os.path.join(path, f))})
##
##
##arr = numpy.array(sizes)
##mean = numpy.mean(arr)
##std =  numpy.std(arr)
##
##arcpy.AddField_management('MEAN')
##arcpy.AddField_management('STD')
##arcpy.AddField_management('ZSCORE')
##
##cur = arcpy.da.UpdateCursor(fc, ['OID@', 'Z_SCORE', 'MEAN', 'STD'])
##
##for row in cur:
##    row[1] = (grids[str(row[0])] - mean)/std
##    row[2] = mean
##    row[3] = std
##    cur.updateRow(row)

