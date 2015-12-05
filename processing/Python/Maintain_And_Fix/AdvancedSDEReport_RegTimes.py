import arcpy, os, datetime, time

arcpy.env.overwriteOutput = True

workPath = r"Database Connections\Connection to cwells.sde"

userHome = os.path.expanduser("~")
folderPath = os.path.join(userHome, "SDETest")

if os.path.exists(folderPath) == False:
    os.mkdir(folderPath)

textFile = open(os.path.join(folderPath, "LogFile.txt"), "w+", 1)
viewName = "GDB_List"

arcpy.env.workspace = workPath


if arcpy.Exists(viewName):
    print "View already exists"
else:
    try:
        arcpy.CreateDatabaseView_management(workPath, viewName, "select owner, table_name, registration_date from sde.table_registry")
    except:
        arcpy.CreateDatabaseView_management(workPath, viewName, "select owner, table_name, registration_date from sde.sde_table_registry")

dbTable = []
timeTable = []

datasets=0
featureClasses=0
tables=0
tableViews=0
rasters=0
spatialViews=0

for row in arcpy.SearchCursor(os.path.join(workPath, viewName)):
    tableName = row.getValue("OWNER") + "." + row.getValue("TABLE_NAME")
    dbTable.append(tableName)
    cDate = row.getValue("REGISTRATION_DATE")
    dTime = time.strftime('%d-%b-%Y %H:%M:%S', time.localtime(cDate))
    timeTable.append(dTime)

datasetList = arcpy.ListDatasets("", "Feature")
datasetList.sort()
for d in datasetList:
    textFile.write("Dataset: " +d+"\n")
    arcpy.env.workspace = os.path.join(workPath, d)
    fcList = arcpy.ListFeatureClasses()
    fcList.sort()
    for fc in fcList:
        #db, tb = fc.split(".", 1)
        desc = arcpy.Describe(fc)
        index = dbTable.index(fc.upper())
        textFile.write("   {0:16}{1:40}{2}".format("Feature Class:",fc.upper(), timeTable[index]))
        textFile.write("\n")
        featureClasses += 1
    tableList = arcpy.ListTables()
    tableList.sort()
    for fc in tableList:
        #db, tb = fc.split(".", 1)
        desc = arcpy.Describe(fc)
        index = dbTable.index(fc.upper())
        textFile.write("   {0:16}{1:40}{2}".format("Table:",fc.upper(), timeTable[index]))
        textFile.write("\n")
        tables += 1
    textFile.write("\n")
    datasets += 1


textFile.write("Geodatabase Objects: \n")
arcpy.env.workspace = os.path.join(workPath)
fcList = arcpy.ListFeatureClasses()
fcList.sort()
for fc in fcList:
    #db, tb = fc.split(".", 1)
    desc = arcpy.Describe(fc)
    if desc.datasetType =="FeatureClass":
        if fc.upper() in dbTable:
            index = dbTable.index(fc.upper())
            textFile.write("   {0:16}{1:40}{2}".format("Feature Class:",fc.upper(), timeTable[index]))
            textFile.write("\n")
            featureClasses += 1
        if fc.upper() not in dbTable:
            textFile.write("   {0:16}{1:40}".format("Spatial View:",fc.upper()))
            textFile.write("\n")
            spatialViews += 1
tableList = arcpy.ListTables()
tableList.sort()
for fc in tableList:
    #db, tb = fc.split(".", 1)
    if fc.upper() in dbTable:
        index = dbTable.index(fc.upper())
        textFile.write("   {0:16}{1:40}{2}".format("Table:",fc.upper(), timeTable[index]))
        textFile.write("\n")
        tables += 1
    if fc.upper() not in dbTable:
        textFile.write("   {0:16}{1:40}".format("Table View:",fc.upper()))
        textFile.write("\n")
        tableViews += 1
for fc in arcpy.ListRasters():
    #db, tb = fc.split(".", 1)
    desc = arcpy.Describe(fc)
    index = dbTable.index(fc.upper())
    textFile.write("   {0:16}{1:40}{2}".format("Raster:",fc.upper(), timeTable[index]))
    textFile.write("\n")
    rasters += 1
textFile.write("\n")

textFile.write("Datasets: " + str(datasets)+"\n")
textFile.write("Feature Classes: "+ str(featureClasses)+"\n")
textFile.write("Tables: " + str(tables)+"\n")
textFile.write("Table Views: " + str(tableViews)+"\n")
textFile.write("Rasters: " + str(rasters)+"\n")
textFile.write("Spatial View: " + str(spatialViews)+"\n")

textFile.close()

arcpy.Delete_management(viewName)
