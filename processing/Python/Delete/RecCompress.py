# Name: ReconcileVersions.py
# Description: Reconciles all versions owned by a user with SDE.Default

# Import system modules
import arcpy, os, sys, datetime, time
from arcpy import env

logFolder = r"C:\gis_scripts\logs\production"


logfileName = os.path.join(logFolder,  "ReconcileCompressLogfile.log")
logfile = open (logfileName,'a')
logfile.write("\n\nStarted: {0} {1}".format(str(time.strftime("%m/%d/%Y")), str(time.strftime("%H:%M:%S"))))

errMsg = arcpy.GetMessages()

# Set workspace

workspace = r'C:\share\DatabaseConnections\SQL\CWELLS101@CWELLS@SQLSERVER@SDE.sde'
# Set the workspace environment
env.workspace = workspace

try:
    # Use a list comprehension to get a list of version names where the owner
    # is the current user and make sure sde.default is not selected.
    verList = [ver.name for ver in arcpy.da.ListVersions() if ver.isOwner == True and ver.name.lower() != 'sde.DEFAULT']
except:
    logfile.write("\nCould not list versions within {0}\nExiting".format(workspace))
    logfile.write("\nFailed: {0} {1}".format(str(time.strftime("%m/%d/%Y")), str(time.strftime("%H:%M:%S"))))
    logfile.write("\n\nArcGIS Messages:\n"+arcpy.GetMessages())
    logfile.close()
    sys.exit(-1)

if len(verList) == 0:
    logfile.write("\nNo versions were returned for {0}\nExiting".format(workspace))
    logfile.write("\nFailed: {0} {1}".format(str(time.strftime("%m/%d/%Y")), str(time.strftime("%H:%M:%S"))))
    logfile.write("\n\nArcGIS Messages:\n"+arcpy.GetMessages())
    logfile.close()
    sys.exit(-1)

try:
    arcpy.ReconcileVersions_management(workspace,
                                       "ALL_VERSIONS",
                                       "sde.DEFAULT",
                                       verList,
                                       "LOCK_ACQUIRED",
                                       "NO_ABORT",
                                       "BY_OBJECT",
                                       "FAVOR_TARGET_VERSION",
                                       "NO_POST",
                                       "KEEP_VERSION",
                                       "")
    logfile.write("\nReconcile versions with SDE.DEFAULT was successful")
except:
    logfile.write("\nReconcile versions with SDE.DEFAULT failed\nExiting")
    logfile.write("\n\nArcGIS Messages:\n"+errMsg)
    logfile.write("\nFailed: {0} {1}".format(str(time.strftime("%m/%d/%Y")), str(time.strftime("%H:%M:%S"))))
    logfile.close()
    sys.exit(-1)

try:
    arcpy.Compress_management(workspace)
    logfile.write("\nCompress for {0} was successful".format(workspace))
except:
    logfile.write("\nCompress for {0} failed\nExiting".format(workspace))
    logfile.write("\nFailed: {0} {1}".format(str(time.strftime("%m/%d/%Y")), str(time.strftime("%H:%M:%S"))))
    logfile.write("\n\nArcGIS Messages:\n"+arcpy.GetMessages())
    logfile.close()
    sys.exit(-1)

logfile.write("\nCompleted: {0} {1}".format(str(time.strftime("%m/%d/%Y")), str(time.strftime("%H:%M:%S"))))
logfile.close()