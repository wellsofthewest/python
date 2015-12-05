import arcpy, os, csv

csvfile = open('C:/temp/pgtest.csv', 'wb')

csvWrite = csv.writer(csvfile, delimiter='|')

gdb = r"Database Connections\Connection to cwells.sde"
fc = r"C:\Users\chri6962\Documents\ArcGIS\Default.gdb\points"

rows = arcpy.da.SearchCursor(fc, ['OBJECTID','SHAPE@WKT'])

for row in rows:
    csvWrite.writerow([row[0], '', row[1]])

csvfile.close()

conn = arcpy.ArcSDESQLExecute(gdb)

sqlCopy = """copy sde.points (objectid, shape, wkt) from 'c:/temp/pgtest.csv' DELIMITER '|' CSV;"""

sqlUpdate = """update sde.points set shape = sde.st_point(wkt, 2272);"""

conn.execute(sqlCopy)

conn.execute(sqlUpdate)
