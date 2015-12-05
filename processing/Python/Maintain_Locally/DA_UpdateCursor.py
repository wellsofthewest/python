import arcpy, os

workspace = r'C:\DatabaseConnections\SQL\CWELLS931@CWELLS@SQLSERVER@SDE.sde'
arcpy.env.workspace=workspace

edit = arcpy.da.Editor(workspace)
edit.startEditing()
edit.startOperation()
field = "PanelNumbe"
rows = arcpy.da.UpdateCursor('cwells931.SDE.FEMA', field, "", "")
for row in rows:
    value = "Hello Jing"
    row[0]=value
    rows.updateRow(row)
edit.stopOperation()
edit.stopEditing(True)