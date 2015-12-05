import arcpy, os

arcpy.env.overwriteOutput = True

#Folder where images are stored MUST BE CHANGED
imgFolder = r"C:\Images"

#Geodatabase where the feature class is stored MUST BE CHANGED
workPath = r"C:\DatabaseConnections\SQL\CWELLS102@CWELLS@SQLSERVER@SDE.sde"

#Feature class to be linked to the images MUST BE CHANGED
fc = r"C:\DatabaseConnections\SQL\CWELLS102@CWELLS@SQLSERVER@SDE.sde\cwells102.SDE.TestDataset\cwells102.SDE.Hello"

#Field within the feature class that contains the name of the file MUST BE CHANGED
imgField = "PanelNumbe"

#Field to be created to store the path of the images
imgPath = "ImagePath"

#Create a table to match to the feature class
tableName = "MatchTable"
table = os.path.join(workPath, tableName)
print table
arcpy.CreateTable_management(workPath, tableName)


#Create the field to store the name and the path
arcpy.AddField_management(table, imgField, "TEXT")
arcpy.AddField_management(table, imgPath, "TEXT")

#Iterate through the feature class to create the path variable
featList = []
rows = arcpy.SearchCursor(fc)
for row in rows:
    fileName = row.getValue(imgField)
    featList.append(fileName)
del row, rows

listLen = len(featList)
cntr = 0
insertRows = arcpy.InsertCursor(table)
for x in xrange(1,96):
    row = insertRows.newRow()
    row.setValue(imgField, featList[cntr])
    row.setValue(imgPath, imgFolder + os.sep + str(featList[cntr]))
    insertRows.insertRow(row)
    cntr += 1

arcpy.EnableAttachments_management(fc)
arcpy.AddAttachments_management(fc, imgField, table, imgField, imgPath)



