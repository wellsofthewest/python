import arcpy

infc = r"C:\Share\DatabaseConnections\SQL\CWELLS101@CWELLS@SQLSERVER@SDE.sde\cwells101.SDE.femapnls"

# Enter for loop for each feature
#
for row in arcpy.da.SearchCursor(infc, ["OID@", "SHAPE@"]):
    if row[1].pointCount < 6:
        print row[0]

