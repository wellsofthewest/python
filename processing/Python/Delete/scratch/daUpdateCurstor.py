import sys
import arcpy
import collections

# POINTS TO MY VERSION OF STAGING:
WORKSPACE = r"C:\Users\chri6962\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\Connection to cwells.sde"
arcpy.env.workspace = WORKSPACE

print "********************** Concatenating parcels easement, opp, row **********************"
parcels = "c1022.SDE.PARCELS_TEST"
fields = ("OID@")
count2 = 0
list = []
print arcpy.GetCount_management(parcels)

edit = arcpy.da.Editor(WORKSPACE)
edit.startEditing(False, True)
edit.startOperation()
with arcpy.da.UpdateCursor(parcels, fields) as updateCur:
    for row in updateCur:
        list.append(str(row[0]))
        count2 += 1
        #updateCur.updateRow(row)
edit.stopOperation()
edit.stopEditing(True)


print count2
print len(list)
