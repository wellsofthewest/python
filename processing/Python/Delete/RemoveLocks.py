import arcpy
from arcpy import env
import sys, string, os, time

# Local variables...
GISADMIN_CodeCasesOpenLocks = 'DOC.New'
GISADMIN_CodeCasesOpenLocksOld = 'DOC.Old'
data_type = "FeatureClass"

# set a variable for the workspace
wsTst2Sde = r'Database Connections\SDE@1022.sde'
wsTst2GISADMIN = r'Database Connections\DOC@1022.sde'

# ALLOW NEW CONNECTIONS TO THE DATABASE.
arcpy.AcceptConnections(wsTst2Sde, True)

 # >>>>>  STEP 1 - DELETE THE OLD VERSION OF THE FEATURE CLASS

# SET THE WORKSPACE
arcpy.env.workspace = wsTst2GISADMIN

# THE OLD VERSION OF THE FEATURE CLASS IS DELETED.
arcpy.Delete_management(GISADMIN_CodeCasesOpenLocksOld)


# ONLY THE USERS FOUND IN THE ARRAY BELOW WILL BE DISCONNECTED FROM THE DATABASE
user_names = ["AGOUSER","STEVEM","GISADMIN"]

# SET THE WORKSPACE - CONNECT TO SDE AS USER SDE
arcpy.env.workspace = wsTst2Sde

# BLOCK NEW CONNECTIONS TO THE DATABASE.
arcpy.AcceptConnections(wsTst2Sde, False)

# RETURNS THE USERS CURRENTLY CONNECTED TO THE DATABASE

connectedUsers = arcpy.ListUsers(wsTst2Sde)
for user in connectedUsers:
    if user.Name in user_names:
        arcpy.DisconnectUser(wsTst2Sde,user.ID)


# ALLOW NEW CONNECTIONS TO THE DATABASE.
arcpy.AcceptConnections(wsTst2Sde, True)

# SET THE WORKSPACE - CONNECT TO SDE AS USER GISADMIN
arcpy.env.workspace = wsTst2GISADMIN

# >>>>> STEP 4 RENAME THE FEATURE CLASS
arcpy.Rename_management(GISADMIN_CodeCasesOpenLocks,'OLD')
print 'DONE'

