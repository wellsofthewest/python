import arcpy
import os
arcpy.env.overwriteOutput = True

arcpy.env.workspace = r"C:\Users\chri0000\Desktop"
fc = r"C:\Users\chri0000\Desktop\one_1.shp"
field = "PARVAL"
valueList = []
valueSet = set()
e = 0
f = 3
g = 5
h = 8
fid = 4

arcpy.AddField_management(fc, "PARV_FIVE", "DOUBLE")
arcpy.AddField_management(fc, "PARV_AVG", "DOUBLE")

rows = arcpy.SearchCursor(fc, "", "", field, "")
for row in rows:
    value = row.getValue(field)
    divvalue = value/5
    if divvalue not in valueSet:
        valueList.append(divvalue)
del row
del rows

i = 0
rowUpdate = arcpy.UpdateCursor(fc, "", "", "PARV_FIVE", "")
for row in rowUpdate:
    row.PARV_FIVE = valueList [i]
    rowUpdate.updateRow(row)
    i = i + 1

del row
del rowUpdate

while fid:
    rowsUpdate = arcpy.UpdateCursor(fc, "\"FID\"   = %s" 'AND' "\"FID\" < 9553" % fid, "", "PARV_AVG", "")
    for row in rowsUpdate:
        average =  (sum(valueList[e:f]) + sum(valueList[g:h]))/8
        row.PARV_AVG = average
        rowsUpdate.updateRow(row)
        fid = fid + 1
        e = e + 1
        f = f + 1
        g = g + 1
        h = h + 1
        print average
        print fid
    del rowsUpdate
        



