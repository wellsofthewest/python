""" CreateReplica.py
    This script checks out a copy of the WeedIncidents and other miscellaneous tables on a PC's C drive. Once the 
    field work/editing is complete the updates can be checked back in with the synChanges.py script.
    
    SCRIPT PARAMETERS:
     server        -s  server from which the layer will be checked out from 
     logfile       -l  logfile path and name
     workarea      -w  a geodatabase were the layer will be copied to
     replicaName   -r  the name of the checked out replica

    EXAMPLE:
     CreateReplica.py -s NT20 -l C:\usr_proj\VegetationMgmt\GDB\OfficeGDB\createRep.log -w C:\usr_proj\ArcGIS\FileGeodatabases\VegetationMgmt\GDB\OfficeGDB\WeedIncidents_FileGDB.gdb -r OfficeReplica
    
    S Long & G Bishop 11/2012 
    """

import sys, getopt, datetime, arcpy, os, logging #, clarkGP
from arcpy import env
#from ScratchName import Scratch
import posixpath as path


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
    server = ''
    logFile = ''
    workArea = ''
    replicaName = ''
    
    try:
	opts, args = getopt.getopt(sys.argv[1:], "hs:l:w:r:", ["iserver=", "ilogfile=", "iworkarea=", "ireplicaName"])	
	for opt, arg in opts:
	    if opt == '-h':
		print 'CreateReplica.py -s <server> -l <logFile> -w <workArea> -r <replicaName>'
		sys.exit(2)
	    elif opt == '-s':
		#server = str((arg).replace(' ', ''))
		server = str((arg).replace("'", ""))
		#server = arg
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
		
	server = server.strip()
	logFile = logFile.strip()
	workArea = workArea.strip()
	replicaName = replicaName.strip()
	    
    except IOError as e:
	print 'CreateReplica script failed: ' + e.message
	sys.exit(2)
    
    var = Variables(server, logFile, workArea)
    
    database_con = Sde_connection(var, server, var.gis_db, replicaName)
    env.workspace = workArea
    
    logging.basicConfig(level=logging.DEBUG,
	                format='%(asctime)s %(levelname)s %(message)s',
	                filename= logFile,
	                filemode='w')
    
    logging.FileHandler(logFile)    
    
    # Check to see if version already exists and bail if it does...
    version_list = arcpy.ListVersions(database_con)
    arcpy.AddMessage("Finished with arcpy.ListVersions")
    for version in version_list:
	#version = version.split(".")[1]
	print version
	logging.info(version)
	if replicaName == version.split(".")[1]:
	    arcpy.AddMessage(replicaName + " already exists")
	    print replicaName + " already exists. Processing stopped."
	    print "Check your replica back in and then rerun the script."
	    sys.exit(0)
    
    tableset = database_con + "\\VegetationMgmt.GIS_SDE.weedIncidents;" + database_con + "\\VegetationMgmt.GIS_SDE.InspectorDistricts;" + database_con + "\\VegetationMgmt.GIS_SDE.weedInfestations;WeedIncidentTypes;BioAgents;Density;Directions;Inspectors;MethodContacted;ROW;Units;weedFollowups;Weeds;WeedTypeRelate;WeedTypes;FollowUpActivities"
    replica_type = "CHECK_OUT"
    output_workspace = workArea
    replica_name = replicaName
    access_type = "FULL"
    initial_sender = "PARENT_DATA_SENDER"
    expand = "USE_DEFAULTS"
    reuse_schema = "DO_NOT_REUSE"
    get_related = "GET_RELATED"
    geometry_feature = ""
    archiving = "DO_NOT_USE_ARCHIVING"
    
    #Remove old workArea and recreate empty file GDB...
    #clarkGP.delete_layer(output_workspace)
    if arcpy.Exists(output_workspace):
	arcpy.Delete_management(output_workspace)
    file_path_gdb,tail = os.path.split(output_workspace)
    print file_path_gdb
    gdb_name, ext_ = os.path.splitext(tail)
    ext = ext_.lower()
    mdb = ".mdb"
    gdb = ".gdb"    
    #print tail
    file_gdb = tail.split(".")[0]
    print file_gdb 
    _log_write(var.log_file, file_gdb)
    
    if not os.path.exists(file_path_gdb):
        os.makedirs(file_path_gdb)
	
    if ext == mdb:
	arcpy.CreatePersonalGDB_management(file_path_gdb, file_gdb)
    elif ext == gdb:
	arcpy.CreateFileGDB_management(file_path_gdb, file_gdb, "CURRENT")
	arcpy.AddMessage("Created Filegeodatabase: " + file_path_gdb + "\\" + file_gdb)
	logging.info("FileGeodatabase Created: " + file_path_gdb + "\\" + file_gdb)
    
    arcpy.MakeTableView_management(database_con + "\\VegetationMgmt.gis_sde.WeedIncidentTypes", "WeedIncidentTypes", "WeedIncidentTypeID > 0")
    arcpy.MakeTableView_management(database_con + "\VegetationMgmt.gis_sde.WEEDFOLLOWUPS", "WEEDFOLLOWUPS", "ObjectID > 0")
    arcpy.MakeTableView_management(database_con + "\VegetationMgmt.gis_sde.Density", "Density", "DensityID > 0")
    arcpy.MakeTableView_management(database_con + "\VegetationMgmt.gis_sde.Directions", "Directions", "DirectionID > 0")
    arcpy.MakeTableView_management(database_con + "\VegetationMgmt.gis_sde.Inspectors", "Inspectors", "InspectorID > 0")
    arcpy.MakeTableView_management(database_con + "\VegetationMgmt.gis_sde.MethodContacted", "MethodContacted", "MethContID > 0")
    arcpy.MakeTableView_management(database_con + "\VegetationMgmt.gis_sde.ROW", "ROW", "ROWID > 0")
    arcpy.MakeTableView_management(database_con + "\VegetationMgmt.gis_sde.Units", "Units", "UnitID > 0")
    arcpy.MakeTableView_management(database_con + "\VegetationMgmt.gis_sde.Weeds", "Weeds", "WeedID > 0")
    arcpy.MakeTableView_management(database_con + "\VegetationMgmt.gis_sde.WeedTypeRelate", "WeedTypeRelate", "ObjectID > 0")
    arcpy.MakeTableView_management(database_con + "\VegetationMgmt.gis_sde.WeedTypes", "WeedTypes", "WeedTypeID > 0")
    arcpy.MakeTableView_management(database_con + "\VegetationMgmt.gis_sde.BioAgents", "BioAgents", "BioAgentID > 0")
    arcpy.MakeTableView_management(database_con + "\VegetationMgmt.gis_sde.FollowUpActivities", "FollowUpActivities", "FollowupActivityID > 0")
    
    # Execute CreateReplica
    try:
	arcpy.CreateReplica_management(tableset, replica_type, output_workspace, replica_name, access_type, initial_sender, expand, reuse_schema, get_related, geometry_feature, archiving)
	logging.info("CreateReplica Completed Successfully")
	arcpy.ClearWorkspaceCache_management(database_con)
	arcpy.ClearWorkspaceCache_management()
    except:
	for i in range(arcpy.GetMessageCount()):
	    _log_write(var.log_file, arcpy.GetMessage(i))
	    error_text = arcpy.GetMessage(i)
	    arcpy.AddMessage(error_text)  
	    logging.info(error_text)
	arcpy.ClearWorkspaceCache_management(database_con)
	arcpy.ClearWorkspaceCache_management()
	#raise Exception(r'Upload to Master failed due to likely collision with another user trying to Upload at the same time.')
    try:
	arcpy.ClearWorkspaceCache_management(database_con)
	arcpy.ClearWorkspaceCache_management()
	os.remove(database_con)
    except IOError as e:
	arcpy.ClearWorkspaceCache_management()
	print("({})".format(e))
    #copyFolder(output_workspace, local_workspace)

def Sde_connection(var, server_name, database_name, replicaName):
    """ 4 arguments:
    connection name (the file that will be instantiated in temp)
    server name (the name of the server you want to connect to)
    database name (the name of the database on the server)
    replica name (the name of the replica that's passed in as the -r arg)
    """
    assert isinstance(var, Variables)
    # Process: Create ArcSDE Connection File...
    # Usage: out_folder_path, out_name, server, service, database, account_authentication, username, password, save_username_password, version,   save_version_info
    #temp = env.scratchFolder
    temp= r"C:\incidents\1249535\myTest"
    # check to make sure the path exists
##    if path.exists(temp) == False:
##	os.mkdir(temp)
##    scratch_obj = Scratch(temp, replicaName, "sde")
       
    #curdir = os.getcwd()
    fileName = "connFile.sde"  #scratch_obj.FileName
    #conn_name = #scratch_obj.FullPathName
    #print conn_name
    
##    try:
##	os.remove(conn_name)
##    except OSError as e:
##	print("file not present")
    #arcpy.AddMessage("temp arg: " + temp + ", fileName arg: " + fileName + ", server_name arg: " + server_name + ", database_name arg: " + database_name)
    arcpy.CreateArcSDEConnectionFile_management(temp, fileName, server_name, 'sde:sqlserver:' + server_name, database_name, 'DATABASE_AUTH'
	                                            , 'gis_sde', 'gis_sde', 'SAVE_USERNAME'
	                                            , 'sde.default', 'SAVE_VERSION')    
    for i in range(arcpy.GetMessageCount()):
	    _log_write(var.log_file, arcpy.GetMessage(i))
	    if "000565" in arcpy.GetMessage(i):   #Check if database connection was successful
		    arcpy.AddReturnMessage(i)
		    _log_write(var.log_file,"+++++Connecting to SDE database FAILED "
		               "Exiting script ++++++++++ ")
		    arcpy.AddMessage("\n connection info: server name: " + server_name 
		                     + " database: " + database_name)
		    arcpy.AddMessage("Exiting!!")
		    arcpy.AddMessage("+++++++++\n")
		    #sys.exit(3)            
	    else:
		    arcpy.AddReturnMessage(i)
		    arcpy.AddMessage("+++++++++\n")
    return(os.path.join(temp, fileName))

def get_filename(curdir):
    
    return(filename)

def _log_write (logFile, message):
    
    (base_path, rep_file_name) = os.path.split(logFile)
    if not os.path.exists(base_path):
        os.makedirs(base_path)
	
    t = datetime.datetime.now() 
    with open(logFile, "a") as f: # r for read, w for write with overwrite, a for append
	f.write(t.strftime("%m/%d/%Y %H:%M:%S:: ") + str(message))
	f.write ("\n")
	f.write ("\n")

	# file auto closed when using "with"
# End of _log_write

if __name__ == '__main__' or sys.argv[0] == __name__:
    main()
