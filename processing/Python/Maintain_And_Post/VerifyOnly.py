import arcpy

grid = r'Database Connections\Connection to gis-db.qa.amwaternp.net (2).sde \GIS_WVAW_South.SDE.Fishnet'
net = r'Database Connections\Connection to gis-db.qa.amwaternp.net (2).sde \GIS_WVAW_South.SDE.NetworkFeatures\GIS_WVAW_South.SDE.Water_Net'

rows = arcpy.da.SearchCursor(grid,["OID@","SHAPE@"])

for row in rows:
    try:
        ext = row[1].extent
        logfile = r"C:\Users\MYSLINAM\Documents\ArcGIS\Water_Fishnet_Test_{0}.txt".format(str(row[0]))
        arcpy.VerifyAndRepairGeometricNetworkConnectivity_management(net, logfile, "VERIFY_ONLY", "EXHAUSTIVE_CHECK", ext)
        print str(row[0]) + " done"
    except:
        print str(row[0]) + " failed"
