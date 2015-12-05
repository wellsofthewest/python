"""
This is an EXAMPLE only of a process to create a connection and 
then upgrade a geodatabase.
"""

# Import system modules
import arcpy
import os

try:
    workspace_path = r"C:\TEMP"
    conn_file = "database_1ss.sde"
# Run the CreateDatabaseConnection tool
    arcpy.CreateDatabaseConnection_management(workspace_path,conn_file,"SQL_SERVER","KENG\KENG","DATABASE_AUTH","arcfm","arcfm","SAVE_USERNAME", "BEHAVIOR")
    print "Connection file created"
except Exception as e:
    print e.message
    arcpy.AddError(e.message)


#Run the upgrade tool using the connection file created above

out_wkspce  = workspace_path + os.sep + conn_file
Default_gdb = workspace_path + os.sep + conn_file
arcpy.UpgradeGDB_management(Default_gdb, "PREREQUISITE_CHECK", "")