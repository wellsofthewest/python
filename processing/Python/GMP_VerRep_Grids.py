import arcpy, os, time
from os import path as p

outdir = p.expanduser('~')
fldname = 'Verify_GN'
gn = r"Database Connections\Connection to gisprd (2).sde\ELEC.ElectricDataset\ELEC.ElecGeomNetwork"

grids = r"C:\Users\esrilocal\Desktop\extFGDB_1.gdb\severityGrids"

if not p.exists(p.join(outdir, fldname)):
    os.mkdir(p.join(outdir, fldname))

rows = arcpy.da.SearchCursor(grids, ["OID@","SHAPE@"])

for row in rows:
    try:
        rowext = row[1].extent
        logfile = p.join(outdir, fldname, "Verify_Grid_{0}.txt".format(str(row[0])))
        start = time.time()
        arcpy.VerifyAndRepairGeometricNetworkConnectivity_management(gn, logfile, "VERIFY_AND_REPAIR", "EXHAUSTIVE_CHECK", rowext)
        stop = time.time()
        timediff = stop-start
        print('Completed Grid OID: {0}'.format(str(row[0])))
        print('\tTime to complete: {0}'.format(timediff))
    except:
        print('Failed to complete Grid OID: {0}'.format(str(row[0])))


