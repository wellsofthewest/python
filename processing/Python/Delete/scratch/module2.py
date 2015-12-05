import arcpy

WORKSPACE = r"C:\Users\chri6962\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\Connection to cwells.sde"
arcpy.env.workspace = WORKSPACE

parcels = "c1022.SDE.RANDOM_POINTS_15K"
fields = ("OID@")
rowCount = 0

edit = arcpy.da.Editor(WORKSPACE)
edit.startEditing(False, True)
edit.startOperation()

updateCur = arcpy.da.UpdateCursor(parcels, fields)
for row in updateCur:
    print row[0]
    rowCount += 1
    updateCur.updateRow(row)
edit.stopOperation()
edit.stopEditing(True)

print str(rowCount) + " Total Row Count."

