import arcpy, os

arcpy.env.overwriteOutput = True

#Location of the existing Mosaic Datasets with Broken Paths
workpath = r"Database Connections\Connection to supt04101.sde"

#Location to create an empty geodatabase
folder = r"C:\Share"

#Location of the individual rasters that have been moved
newGDB = r"C:\Share\From_Julia\Amberg_tif2\Amberg_tif2"

#Create Scratch GDB
scratch = folder + os.sep + "Scratch.gdb"
arcpy.CreateFileGDB_management(folder, "Scratch")

#Set workspace
arcpy.env.workspace = workpath

#List Mosaic Datasets
dsList = arcpy.ListDatasets("", "Mosaic")

#Get Mosaic Dataset Paths
dsPath = []
for ds in dsList:
    print ds
    try:
        arcpy.ExportMosaicDatasetPaths_management(ds, os.path.join(scratch, ds), "#", "ALL", "RASTER")
    except:
        dsPath.append(workpath+os.sep+ds)

#Set scratch workspace
arcpy.env.workspace = scratch

#List Tables of MD Paths
##tableList = arcpy.ListTables()
##cntr = 0
##for table in tableList:
##    rows = arcpy.SearchCursor(table)
##
##    #Search tables for MD paths
##    for row in rows:
##        path = row.getValue("Path")
##        print table
##        print path
##        dir = os.path.dirname(path)
##        ov = dir.endswith("Overviews")
##
##        #Filter directories to ignore Overviews
##        if ov == False:
##                fileName = os.path.basename(path)
##                name, extension = os.path.splitext(fileName)
##                inputPath = dir + " " + newGDB
##
##                #Create SQL Query based on raster path
##                sql = """ "Name" = '{0}' """.format(name)
##
##                #Repair MD Path
##                arcpy.RepairMosaicDatasetPaths_management(dsPath[cntr], inputPath, sql)
##    cntr += 1

#Delete variables
#del table, tableList, dsList, row, rows

#Delete Scratch Workspace
#arcpy.Delete_management(scratch)

