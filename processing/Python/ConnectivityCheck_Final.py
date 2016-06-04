import arcpy, os, math, numpy
from os import path as p

#Path to the geometric network
gn = r"Database Connections\Elec.Dataset\Elec.GN"

#Path to a feature class that represents the extent of the network distribution
fc = r"Database Connections\Elec.Dataset\Elec.PriOHLine"
ext = arcpy.Describe(fc).extent

#Gather the feature dataset name
fd = p.dirname(gn)

#Gather the GDB name
gdb = p.dirname(fd)

#TEMP FGDB Name
gdbname = 'extFGDB.gdb'

#TEMP Fishnet Grid Name
extname = 'extGrids'

#TEMP Output Location (Default: echo %USERPROFILE%)
outdir = p.expanduser('~')

#TEMP Folder Name
fldname = 'Verify_GN'

arcpy.env.outputCoordinateSystem = fc

#If TEMP folder does not exist, create it
if not p.exists(p.join(outdir, fldname)):
    os.mkdir(p.join(outdir, fldname))

outfc = p.join(outdir, fldname, gdbname, extname)

#If TEMP FGDB does not exist, create it
if not p.exists(p.join(outdir, fldname, gdbname)):
    arcpy.CreateFileGDB_management(p.join(outdir, fldname), gdbname)

#Specify Fishnet grid sizes (5000 represents spatial reference with units = FT)
xgrids = 2000
ygrids = 2000

#Delete the TEMP Fishnet, if it exists
if arcpy.Exists(outfc):
    arcpy.Delete_management(outfc)

#Gather extent information for Fishnet
stpnt = "{0} {1}".format(ext.XMin, ext.YMin)
ypnt = "{0} {1}".format(ext.XMin, ext.YMin+1)
endpnt = "{0} {1}".format(ext.XMax, ext.YMax)

#Create Fishnet
arcpy.CreateFishnet_management(out_feature_class=outfc,
                               origin_coord=stpnt,
                               y_axis_coord=ypnt,
                               cell_width=ygrids,
                               cell_height=xgrids,
                               corner_coord=endpnt,
                               labels="NO_LABELS",
                               geometry_type="POLYGON")

#Prepare the GN Feature Class and Fishnet Feature Class to be queried
lyrGrid = arcpy.MakeFeatureLayer_management(outfc, 'lyrGrid')
lyrFC = arcpy.MakeFeatureLayer_management(fc, 'lyrFC')

#Query GN FC + Fishnet FC for intersection, then delete non-intersecting parts
arcpy.SelectLayerByLocation_management(lyrGrid, 'INTERSECT', lyrFC)
arcpy.SelectLayerByAttribute_management(lyrGrid, 'SWITCH_SELECTION')
arcpy.DeleteFeatures_management(lyrGrid)

#Create Search Cursor to loop through grids to verify connectivity
rows = arcpy.da.SearchCursor(outfc, ["OID@","SHAPE@"])

for row in rows:
    try:
        rowext = row[1].extent
        logfile = p.join(outdir, fldname, "Verify_Grid_{0}.txt".format(str(row[0])))
        #Parameter verify_or_repair can have the following options:
        #VERIFY_ONLY ?	Run verification checks for the geometric network for connectivity errors but do not perform repair. This is the default.
        #VERIFY_AND_REPAIR ?After completion of the verification checks, perform repair of the connectivity errors.
        arcpy.VerifyAndRepairGeometricNetworkConnectivity_management(gn, logfile, verify_or_repair="VERIFY_AND_REPAIR", "EXHAUSTIVE_CHECK", rowext)
    except:
        arcpy.AddMessage('Errors in Grid OID: {0}'.format(str(row[0])))

#Analyze grids for statistics
sizes = []
grids = {}

#Find the size of each error log
for f in os.listdir(p.join(outdir, fldname)):
    sizes.append(os.path.getsize(p.join(outdir, fldname, f)))
    grids.update({'{}'.format(p.splitext(f[12:])[0]):p.getsize(p.join(outdir, fldname, f))})


arr = numpy.array(sizes)
mean = numpy.mean(arr)
std =  numpy.std(arr)

arcpy.AddField_management(p.join(outdir, fldname, gdbname, extname),'MEAN', "DOUBLE")
arcpy.AddField_management(p.join(outdir, fldname, gdbname, extname),'STD', "DOUBLE")
arcpy.AddField_management(p.join(outdir, fldname, gdbname, extname),'ZSCORE', "DOUBLE")

#Insert mean, standard deviation, and z-score into the grids feature class
cur = arcpy.da.UpdateCursor(p.join(outdir, fldname, gdbname, extname), ['OID@', 'Z_SCORE', 'MEAN', 'STD'])

for row in cur:
    row[1] = (grids[str(row[0])] - mean)/std
    row[2] = mean
    row[3] = std
    cur.updateRow(row)

