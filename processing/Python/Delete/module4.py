import arcpy

csv =  r"C:\share\test.csv"

rows = arcpy.SearchCursor(csv)

string = "INSERT INTO WFS.CHRIS (OBJECTID,SDO_SHAPE) VALUES ({0}, SDO_UTIL.FROM_WKTGEOMETRY('{1}'));"

CNT = 0
for row in rows:
    CNT +=1
##    wkt = row.getValue("WKT")
##    oid = row.getValue("objectid")
##    print string.format(oid, wkt)

print CNT