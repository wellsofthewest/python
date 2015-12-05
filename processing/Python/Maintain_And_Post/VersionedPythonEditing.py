# Import system modules
import arcpy, os
from arcpy import env

# Set workspace

#Please place your database connection here
workspace = r'C:\share\DatabaseConnections\SQL\CWELLS101@CWELLS@SQLSERVER@SDE.sde'

# Set the workspace environment
env.workspace = workspace

#Calculate XY Data

#Please place your path to the features here
table = r"C:\share\DatabaseConnections\SQL\CWELLS101@CWELLS@SQLSERVER@SDE.sde\cwells101.SDE.FEMA"
arcpy.MakeFeatureLayer_management(table, "Polygon")
arcpy.ChangeVersion_management("Polygon", "TRANSACTIONAL", "sde.Insert")
edit = arcpy.da.Editor(workspace)

# Edit session is started without an undo/redo stack for versioned data
# (for second argument, use False for unversioned data)
edit.startEditing(False, True)
print "Starting edit session..."

# Start an edit operation
edit.startOperation()

#Calculate XY values in WGS 1984

field = "url"
print "\nUpdating rows..."
rows = arcpy.da.UpdateCursor("Polygon", [field],"","")
for row in rows:
    value = "BAT_FileTest"
    row[0]=value #DA Cursor
    rows.updateRow(row)


print "\tRows updated..."

edit.stopOperation()

# Stop the edit session and save the changes
edit.stopEditing(True)
print "\nEdit session stopped"
