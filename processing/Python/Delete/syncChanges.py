""" syncChanges.py
    This script checks back in a copy of the WeedIncidents layer to sde which has been checked out 
    with the CreateRepica.py script.
    
    SCRIPT PARAMETERS:
     server        -s  server from which the layer will be checked out from 
     logfile       -l  logfile path and name
     workarea      -w  a geodatabase were the layer will be copied to
     replicaName   -r  the name of the checked out replica

    EXAMPLE:
     synChanges.py -s NT20 -l C:\usr_proj\createRep.log -w C:\usr_proj\ArcGIS\FileGeodatabases\VegetationMgmt\WeedIncidents_FileGDB.gdb -r MarkReplica
    
    S Long 11/2012 
    """
import sys, getopt, datetime, arcpy, os, logging, time
from arcpy import env
#from ScratchName import Scratch

arcpy.env.overwriteOutput = True


class Variables: 
    def __init__(self, server, logFile, workArea):
	# set up project variables	
	self.gis_server = server
	self.gis_db = r'VegetationMgmt'
	self.workarea = workArea
	self.log_file = logFile
	print self.log_file

def main():
    
    # set variables...
    server = ''
    logFile = ''
    workArea = ''
    replicaName = ''
    
    #pause execution for 2 seconds....
    print "Start : %s" % time.ctime()
    time.sleep(2)
    print "End : %s" % time.ctime()  
    
    try:
	opts, args = getopt.getopt(sys.argv[1:], "hs:l:w:r:", ["iserver=", "ilogfile=", "iworkarea=", "ireplicaName"])
	for opt, arg in opts:
	    if opt == '-h':
		print 'syncChanges.py -s <server> -l <logFile> -w <workArea> -r <replicaName>'
		sys.exit(2)
	    elif opt == '-s':
		#server = arg
		#server = str((arg).replace(' ', ''))
		server = str((arg).replace("'", ""))
	    elif opt == '-l':
		#logFile = arg
		#logFile = str((arg).replace(' ', ''))
		logFile = str((arg).replace("'", ""))
	    elif opt == '-w':
		#workArea = arg
		#workArea = str((arg).replace(' ', ''))
		workArea = str((arg).replace("'", ""))
	    elif opt == '-r':
		#replicaName = arg
		#replicaName = str((arg).replace(' ', ''))
		replicaName = str((arg).replace("'", ""))
    except IOError as e:
	print 'syncChanges script failed: ' + e.message
	sys.exit(2)
	
    #Code below is needed for web service...	
    server = server.strip()
    logFile = logFile.strip()
    workArea = workArea.strip()
    replicaName = replicaName.strip()    

    var = Variables(server, logFile, workArea)   
    
    database_con = Sde_connection(var, server, var.gis_db, replicaName)
##    if not os.path.exists(var.workarea):
##	os.makedirs(var.workarea)    
    env.workspace = workArea
    
    #Check to see if replica exists...
    rep_found = check_for_replica(database_con,replicaName)
    
    # Check to see if version exists...
    version_found = check_for_version(database_con, var, replicaName)
	    
    # If orphan replica, delete version....
    if version_found and not rep_found:
	arcpy.DeleteVersion_management(database_con, replicaName)
	print "Orphan version found for " + replicaName +". Deleting this version."
	logging.info("Orphan version found for " + replicaName +". Deleting this version.")
	arcpy.ClearWorkspaceCache_management(database_con)
	os.remove(database_con)	
	sys.exit(0)    

    if not version_found and not rep_found:
	print("You do not have a replica to check in.")
	logging.info("You do not have a replica to check in.")
	arcpy.ClearWorkspaceCache_management(database_con)
	os.remove(database_con)
	sys.exit()
    
    replica_gdb1 = workArea
    replica_gdb2 = database_con
    replica_name = replicaName
    sync_direction = "FROM_GEODATABASE1_TO_2"
    conflict_policy = "IN_FAVOR_OF_GDB1" 	# applicable for CHECKOUT replicas.
    conflict_detection = "BY_OBJECT"            # applicable for CHECHOUT replicas.
    reconcile = "RECONCILE "                    # applicable for CHECHOUT replicas.  This line needs a test to confirm this is the correct string
                                                # for this variable
    # Execute SynchronizeChanges
    try:
	arcpy.SynchronizeChanges_management(replica_gdb1, replica_name, replica_gdb2, sync_direction, conflict_policy, conflict_detection, reconcile)    
    except:
	for i in range(arcpy.GetMessageCount()):
	    _log_write(var.log_file, arcpy.GetMessage(i))
	    error_text = arcpy.GetMessage(i)
	    arcpy.AddMessage(error_text)
	arcpy.ClearWorkspaceCache_management(database_con)

    try:
	arcpy.ClearWorkspaceCache_management(database_con)
	os.remove(database_con)
    except IOError as e:
	print("({})".format(e))    
    
def Sde_connection(var, server_name, database_name, replicaName):
    """ 4 arguments:
    connection name (the file that will be instantiated in temp)
    server name (the name of the server you want to connect to)
    database name (the name of the database on the server)
    replica name (the name of the replica passed as an arg to the script)
    """
    assert isinstance(var, Variables)
    # Process: Create ArcSDE Connection File...
    # Usage: out_folder_path, out_name, server, service, database, account_authentication, username, password, save_username_password, version,   save_version_info
    
    temp = r"C:\incidents\1249535\myTest"  # env.scratchFolder
##    # check to make sure the path exists
##    if os.path.exists(temp) == False:
##	os.mkdir(temp)    
##    scratch_obj = Scratch(temp, replicaName, "sde")
       
    fileName =  "synConn.sde"  #scratch_obj.FileName
    #conn_name = scratch_obj.FullPathName
    #print conn_name    
    
    #curdir = os.getcwd()  
    ##fileName = database_name + '_' + server_name + '.' + "sde"
    #fileName = replicaName + ".sde"
    #conn_name = curdir + os.sep + fileName
    #print conn_name
    
##    try:
##	os.remove(conn_name)
##    except OSError as e:
##	print("file not present")
    
    arcpy.CreateArcSDEConnectionFile_management(temp, fileName, server_name, 'sde:sqlserver:' + server_name, database_name, 'DATABASE_AUTH'
	                                            , 'gis_sde', 'gis_sde', 'SAVE_USERNAME'
	                                            , 'sde.default', 'SAVE_VERSION')    
    for i in range(arcpy.GetMessageCount()):
	_log_write(var.log_file, arcpy.GetMessage(i))
	if "000565" in arcpy.GetMessage(i):   #Check if database connection was successful
	    arcpy.AddReturnMessage(i)
	    _log_write(var.log_file,"+++++Connecting to SDE database FAILED "
	               "Exiting script ++++++++++ ")
	    arcpy.AddMessage("\n connection info: server name: " + server_name + " database: " + database_name)
	    arcpy.AddMessage("Exiting!!")
	    arcpy.AddMessage("+++++++++\n")
	    #sys.exit(3)            
	else:
	    arcpy.AddReturnMessage(i)
	    arcpy.AddMessage("+++++++++\n")
    return(os.path.join(temp, fileName))   #(conn_name)

def check_for_replica(database_con,replicaName):
    GDB_items_sde = database_con + os.sep + "VegetationMgmt.sde.GDB_ITEMS"
    rep_found = False
    repCursor = arcpy.SearchCursor(GDB_items_sde, "TYPE='4ED4A58E-621F-4043-95ED-850FBA45FCBC'", "", "NAME")
    for cur in repCursor:
	if cur.name == replicaName:
	    print cur.name
	    rep_found = True    
    print "rep_found = " + str(rep_found)
    del cur, repCursor
    return(rep_found)

def check_for_version(database_con, var, replicaName):
    # Check to see if version exists...
   
##    temp = env.scratchFolder
##    # check to make sure the path exists
##    if os.path.exists(temp) == False:
##	os.mkdir(temp)
##	
##    scratch_obj = Scratch(temp, replicaName, "sde")
##    fileName = scratch_obj.FileName
##    db_con = scratch_obj.FullPathName
##    arcpy.CreateArcSDEConnectionFile_management(temp, fileName, var.gis_server, 'sde:sqlserver:' + var.gis_server, var.gis_db, 'DATABASE_AUTH'
##	                                            , 'gis_sde', 'gis_sde', 'SAVE_USERNAME'
##	                                            , 'sde.default', 'SAVE_VERSION') 
    versions_sde = database_con + os.sep + "VegetationMgmt.sde.sde_versions"
    items_view = "items_view"
    arcpy.MakeTableView_management(versions_sde, items_view, "", "", "")
    result = int(arcpy.GetCount_management(items_view).getOutput(0)) 
    print "The count of items_sde is " + str(result)
    ver_found = False
    if result > 0:
	rows = arcpy.SearchCursor(items_view)
	for row in rows:
	    print row.name
	    if row.name == replicaName:
		ver_found = True
	del row, rows
    arcpy.ClearWorkspaceCache_management(database_con)
    #os.remove(db_con)
    print "version_found = " + str(ver_found)
    return(ver_found)

def _log_write (logFile, message):
    t = datetime.datetime.now() 
    with open(logFile, 'a') as f: # r for read, w for write with overwrite, a for append
	f.write(t.strftime("%m/%d/%Y %H:%M:%S:: ") + str(message))
	f.write ("\n")
	f.write ("\n")
	# file auto closed when using "with"
# End of _log_write

if __name__ == '__main__' or sys.argv[0] == __name__:
    main()
