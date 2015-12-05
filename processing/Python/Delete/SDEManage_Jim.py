# SDEManage.py
#
# This program manages these nightly SDE tasks:
#   Check     <Oracle Instance>
#	Compress  <Oracle Instance>
#	Cook      <Oracle Instance> (not implemented)
#	Reconcile <Oracle Instance>
#	Replicate <Oracle Instance From> <Oracle Instance To>
#
# Location:    G:\GIS\Run\ArcSDE
# Languages:   ArcGIS 10.2.1, Python 2.7.3, Oracle 11g, SQL Server 2012
# Last Change: 02/28/2014 Tom Elder, Jim Jarvis
# Reconcile:  Added in Wei Gao 7/2011

import arcpy, cx_Oracle, datetime, os, string, sys, win32com.client
from arcpy import env 
import sys, re, time, traceback
import sqlite3, os.path
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.MIMEText import MIMEText

print ""
print "SDE Manager         START", datetime.datetime.now().strftime("%a %d %b %Y %H:%M:%S")



#=============================================================================================================================
# ARGUMENTS: Enter the program to run (reconcile, compress, replicate) and the Oracle instance (sdwp, sdlp, sdep, etc.) as
#            arguments. Replicate needs a third argument for the Oracle instance to replicate to (sdep, etc.).
#=============================================================================================================================

# Stop the program if no arguments have been provided.
try:
   Task = sys.argv[1]
   Task = str.upper(Task)
except:
   print "Usage: check     <Oracle Instance>"
   print "       compress  <Oracle Instance>"
   print "       cook      <Oracle Instance>"
   print "       reconcile <Oracle Instance>"
   print "       replicate <Oracle Instance From> <Oracle Instance To>"
   sys.exit()

### Stop the program if the task is incorrect or has been mistyped.

if  Task not in ("CHECK", "COMPRESS", "COOK", "RECONCILE", "REPLICATE"):
   print Task + "? Enter check, compress, cook, reconcile, or replicate."
   sys.exit()

# Stop the program if the Oracle instance has not been provided.

try:
   OracleInstance = sys.argv[2]
   OracleInstance = str.upper(OracleInstance)

except:
   if Task == "REPLICATE":
      print Task, "<Oracle Instance From> <Oracle Instance To>"
   else:
      print Task, "<Oracle Instance>"
   sys.exit()

# Stop the program if the task is replicate and the Oracle instance to replicate to has not been provided.

if Task == "REPLICATE":
   try:
      OracleInstanceTo = sys.argv[3]
      OracleInstanceTo = str.upper(OracleInstanceTo)
   except:
      print Task, OracleInstance, "<Oracle Instance To>"
      sys.exit()
else:
   OracleInstanceTo = "NONE" # To avoid the use of many, many more if statements.

#=============================================================================================================================
# Connect to the GIS Data Management database and check the SCHEDULE table for the run time and day for the task.
#=============================================================================================================================

SQLServerConnection = win32com.client.Dispatch("ADODB.Connection")
SQLServerConnection.Open("Provider=SQLOLEDB.1;Data Source=EntPrd12\EntPrd12;uid=gisrun;pwd=G1Sguru!;database=MapServices")

try:
   SQLServerConnection.State
   print "SQL Server          OK"
except:
   print "SQL Server          ERROR"

# Record the start of the program.

Host  = os.getenv("COMPUTERNAME")
Login = os.getenv("USERNAME")

SQLServerConnection.execute("INSERT INTO MapServices.dbo.LOG (TIME_STAMP, PROGRAM, SERVER, LOGIN, INSTANCE, INSTANCE_TO, STATUS, DETAIL) VALUES (GETDATE(),'" + Task + "','" + Host + "','" + Login + "','" + OracleInstance + "','" + OracleInstanceTo + "','START',NULL)")

# Get the start time and date for the task. Stop the program if there is no record in the SCHEDULE table.
# Note: The start and end times are stored and handled as integers to simplify data conversion.

SQLServerCursor = win32com.client.Dispatch('ADODB.Recordset')
SQLServerCursor.Open("SELECT START_TIME, END_TIME, START_DAY, END_DAY, ORACLE_SCHEMA FROM MapServices.dbo.SCHEDULE WHERE PROGRAM = '" + Task + "' AND ORACLE_INSTANCE = '" + OracleInstance + "' AND ORACLE_INSTANCE_TO = '" + OracleInstanceTo + "'", SQLServerConnection, 1, 3)

if not SQLServerCursor.EOF:
   SQLServerCursor.MoveFirst()
   while not SQLServerCursor.EOF:
      StartTime    = int(SQLServerCursor.Fields("START_TIME").Value)
      EndTime      = int(SQLServerCursor.Fields("END_TIME").Value)
      StartDay     = int(SQLServerCursor.Fields("START_DAY").Value)
      EndDay       = int(SQLServerCursor.Fields("END_DAY").Value)
      OracleSchema = SQLServerCursor.Fields("ORACLE_SCHEMA").Value
      ##print Task, OracleInstance, OracleInstanceTo, StartTime, EndTime, StartDay, EndDay, OracleSchema
      SQLServerCursor.MoveNext()
else:
   print "Schedule            ERROR", Task, OracleInstance, OracleInstanceTo, "has no record in the SCHEDULE table."
   SQLServerConnection.execute("INSERT INTO MapServices.dbo.LOG (TIME_STAMP, PROGRAM, SERVER, LOGIN, INSTANCE, INSTANCE_TO, STATUS, DETAIL) VALUES (GETDATE(), '" + Task + "','" + Host + "','" + Login + "','" + OracleInstance+ "','" + OracleInstanceTo + "','ERROR','No record was found in the SCHEDULE table')")
   sys.exit()

SQLServerCursor.close

#=============================================================================================================================
# Check the time of the day.
#=============================================================================================================================

TimeOfDay = int(datetime.datetime.now().strftime("%H%M"))
if TimeOfDay >= StartTime and TimeOfDay < EndTime:
   print "Time                OK", TimeOfDay
else:
   print "Time                ERROR Time out of range", TimeOfDay
   ##SQLServerConnection.execute("INSERT INTO MapServices.dbo.LOG (TIME_STAMP, PROGRAM, SERVER, LOGIN, INSTANCE, INSTANCE_TO, STATUS, DETAIL) VALUES (GETDATE(), '" + Task + "','" + Host + "','" + Login + "','" + OracleInstance+ "','" + OracleInstanceTo + "','ERROR','Time out of range " + repr(TimeOfDay) + "')")
   ##sys.exit()

#=============================================================================================================================
# Check the day of week.
#=============================================================================================================================

DayOfWeek = datetime.datetime.now().weekday()
if DayOfWeek >= StartDay and DayOfWeek <= EndDay:
   print "Day                 OK", DayOfWeek
else:
   print "Day                 ERROR Day out of range.", DayOfWeek
   SQLServerConnection.execute("INSERT INTO MapServices.dbo.LOG (TIME_STAMP, PROGRAM, SERVER, LOGIN, INSTANCE, INSTANCE_TO, STATUS, DETAIL) VALUES (GETDATE(), '" + Task + "','" + Host + "','" + Login + "','" + OracleInstance+ "','" + OracleInstanceTo + "','ERROR','Day out of range " + repr(DayOfWeek) + "')")
   sys.exit()

#=============================================================================================================================
# Check the Oracle connection.
#=============================================================================================================================

if OracleInstance != "NONE":

   try:
      OracleConnection = cx_Oracle.connect("GISREAD/GISREAD1@" + OracleInstance)
      OracleCursor = OracleConnection.cursor()
      print "Oracle              OK", OracleInstance, OracleConnection.version

   except cx_Oracle.DatabaseError, OracleError:
      print "Oracle              ERROR", OracleInstance, str(OracleError).rstrip()
      SQLServerConnection.execute("INSERT INTO MapServices.dbo.LOG (TIME_STAMP, PROGRAM, SERVER, LOGIN, INSTANCE, INSTANCE_TO, STATUS, DETAIL) VALUES (GETDATE(), '" + Task + "','" + Host + "','" + Login + "','" + OracleInstance+ "','" + OracleInstanceTo + "','ERROR','" + str(OracleError).rstrip() + "')")
      sys.exit()

#=============================================================================================================================
# Check the Oracle connection to if replicating.
#=============================================================================================================================

if Task == "REPLICATE" and OracleInstanceTo not in ("GISADM","LNDADM","WTRADM"):
   try:
      OracleConnectionTo = cx_Oracle.connect("GISREAD/GISREAD1@" + OracleInstanceTo)
      OracleCursorTo = OracleConnectionTo.cursor()
      print "Oracle To           OK", OracleInstanceTo, OracleConnectionTo.version

   except cx_Oracle.DatabaseError, OracleError:
      print "Oracle To           ERROR", OracleInstanceTo, str(OracleError).rstrip()
      SQLServerConnection.execute("INSERT INTO MapServices.dbo.LOG (TIME_STAMP, PROGRAM, SERVER, LOGIN, INSTANCE, INSTANCE_TO, STATUS, DETAIL) VALUES (GETDATE(), '" + Task + "','" + Host + "','" + Login + "','" + OracleInstance+ "','" + OracleInstanceTo + "','ERROR','" + str(OracleError).rstrip() + "')")
      sys.exit()

#=============================================================================================================================
# Check the SDE connection.
#=============================================================================================================================

if OracleInstance != "NONE":

   SQLServerCursor.Open("SELECT SDE_HOST, SDE_PORT FROM MapServices.dbo.DATABASES WHERE ORACLE_INSTANCE = '" + OracleInstance + "'", SQLServerConnection, 1, 3)

   if not SQLServerCursor.EOF:
      SQLServerCursor.MoveFirst()
      while not SQLServerCursor.EOF:
         SDEServer = str(SQLServerCursor.Fields("SDE_HOST").Value)
         SDEPort   = str(SQLServerCursor.Fields("SDE_PORT").Value)
         SQLServerCursor.MoveNext()
   else:
      print "SDE                 ERROR No record found in the Databases table"
      SQLServerConnection.execute("INSERT INTO MapServices.dbo.LOG (TIME_STAMP, PROGRAM, SERVER, LOGIN, INSTANCE, INSTANCE_TO, STATUS, DETAIL) VALUES (GETDATE(), '" + Task + "','" + Host + "','" + Login + "','" + OracleInstance+ "','" + OracleInstanceTo + "','ERROR','No record for SDE host or port was found in the Databases table')")
      sys.exit()

   SQLServerCursor.close
   SDEError = os.system("sdemon -o status -s " + SDEServer + " -i " + SDEPort + ">>F:\\GIS\\Logs\\SDECheck.log")

##   if   SDEError == 0:
##      print "SDE                 OK", OracleInstance
##   else:
##      print "SDE                 ERROR", OracleInstance, SDEError, "Check the last lines in F:\GIS\Logs\SDECheck.log"
##      SQLServerConnection.execute("INSERT INTO MapServices.dbo.LOG (TIME_STAMP, PROGRAM, SERVER, LOGIN, INSTANCE, INSTANCE_TO, STATUS, DETAIL) VALUES (GETDATE(), '" + Task + "','" + Host + "','" + Login + "','" + OracleInstance+ "','" + OracleInstanceTo + "','ERROR','SDE other error code " + repr(SDEError) + "')")
##      sys.exit()

#=============================================================================================================================
# Check the SDE connection to replicate to.
#=============================================================================================================================

if Task == "REPLICATE" and OracleInstanceTo not in ("GISADM","LNDADM","WTRADM"):
   SQLServerCursor.Open("SELECT SDE_HOST, SDE_PORT FROM Databases WHERE ORACLE_INSTANCE = '" + OracleInstanceTo + " '", SQLServerConnection, 1, 3)
   if not SQLServerCursor.EOF:
      SQLServerCursor.MoveFirst()
      while not SQLServerCursor.EOF:
         SDEServerTo = str(SQLServerCursor.Fields("SDE_HOST").Value)
         SDEPortTo   = str(SQLServerCursor.Fields("SDE_PORT").Value)
         SQLServerCursor.MoveNext()
   else:
      print "SDE To              ERROR No record in the Databases table"
      SQLServerConnection.execute("INSERT INTO MapServices.dbo.LOG (TIME_STAMP, PROGRAM, SERVER, LOGIN, INSTANCE, INSTANCE_TO, STATUS, DETAIL) VALUES (GETDATE(), '" + Task + "','" + Host + "','" + Login + "','" + OracleInstance+ "','" + OracleInstanceTo + "','ERROR','No record for SDE host or port " + OracleInstanceTo + " was found in the Databases table')")
      sys.exit()

   SQLServerCursor.close

   SDEErrorTo = os.system("sdemon -o status -s " + SDEServerTo + " -i " + SDEPortTo + ">>F:\\GIS\\Logs\\SDECheck.log")
   if   SDEErrorTo == 0:
      print "SDE To              OK", OracleInstanceTo
   else:
      print "SDE To              ERROR", OracleInstanceTo, SDEErrorTo, "Check the last lines in F:\GIS\Logs\SDECheck.log"
      SQLServerConnection.execute("INSERT INTO MapServices.dbo.LOG (TIME_STAMP, PROGRAM, SERVER, LOGIN, INSTANCE, INSTANCE_TO, STATUS, DETAIL) VALUES (GETDATE(), '" + Task + "','" + Host + "','" + Login + "','" + OracleInstance+ "','" + OracleInstanceTo + "','ERROR','SDE other error code " + repr(SDEErrorTo) + "')")
      sys.exit()

#=============================================================================================================================
# CHECK module
#=============================================================================================================================

if Task == "CHECK":

   print "CHECK               OK", OracleInstance
   SQLServerConnection.execute("INSERT INTO MapServices.dbo.LOG (TIME_STAMP, PROGRAM, SERVER, LOGIN, INSTANCE, INSTANCE_TO, STATUS, DETAIL) VALUES (GETDATE(), '" + Task + "','" + Host + "','" + Login + "','" + OracleInstance+ "','" + OracleInstanceTo + "','STOP','Completed successfully')")

#=============================================================================================================================
# RECONCILE module by Jim Jarvis 2/2014
#=============================================================================================================================

if Task == "RECONCILE":

    ## Report file name and locations
    reportTime = datetime.datetime.now().strftime("%Y-%m-%d")
    preFile = "F:/GIS/Logs/AutoReconcile/reconcilePre_" + OracleInstance+ "_%s.txt" %reportTime
    defFile = "F:/GIS/Logs/AutoReconcile/reconcileDef_" + OracleInstance+ "_%s.txt" %reportTime
    if os.path.exists(preFile):
       os.remove(preFile)

    try:
        SDEConnection = "B:/Public/GIS/Service/Database Connections/" + OracleInstance+ "_SDE.sde"
        gisRead = OracleConnection
        
        ## Variables: log file, counters for conflict and error
        sCode = 0
        lines = ""
        cCount = 0
        eCount = 0

        ## Get a list of connected users.
        userList = arcpy.ListUsers(SDEConnection)

        ## Get a list of user names of users currently connected and make email addresses
        #emailList = [u.Name + "@yourcompany.com" for user in arcpy.ListUsers(SDEConnection)]
        emailList = ["james.jarvis" + "@phoenix.gov"]# for user in arcpy.ListUsers(SDEConnection)]

        ## Take the email list and use it to send an email to connected users.
        SERVER = "DOMSMTP01"
        FROM = "SDE Admin <james.jarvis@phoenix.gov>"
        TO = emailList
        SUBJECT = "Maintenance is about to be performed"
        MSG = "Auto generated Message.\n\rServer maintenance will be performed in 15 minutes. Please log off."

        ## Prepare actual message
        MESSAGE = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (FROM, ", ".join(TO), SUBJECT, MSG)

        ## Send the mail
        server = smtplib.SMTP(SERVER)
        server.sendmail(FROM, TO, MESSAGE)
        server.quit()

        ## Block new connections to the database.
        #arcpy.AcceptConnections(SDEConnection, False)

        ## Wait 15 minutes
        #time.sleep(900)

        ## Disconnect all users from the database.
        #arcpy.DisconnectUser(SDEConnection, "ALL")

        ## Get a list of versions to pass into the ReconcileVersions tool.
        versionList = arcpy.ListVersions(SDEConnection)
        ## Retrieve preaccept list
        #preList = [ver.name for ver in arcpy.da.ListVersions(SDEConnection) if ver.children
        #           and ver.name.lower() != 'sde.default'] 
        ## Retrieve child versions for each preaccept
        preChildList = []
        for version in arcpy.da.ListVersions(SDEConnection):
            if version.parentVersionName != 'SDE.DEFAULT' and version.name != 'SDE.DEFAULT':
                preChildList.append(version.name)   
        ## Create a cursor for the target version list

        #theTargets = gisRead.cursor()
        preList = [version.name for version in arcpy.da.ListVersions(SDEConnection) if version.children
                   and version.name.lower() != 'sde.default']
        print "Here I am 1!"
        print preList
        #theTargets.execute(preList)
        
        ## Execute the ReconcileVersions tool.
        print "Here I am 2!"
        #for tarEach in theTargets.fetchall():
        for tarEach in preList:
           theTarget = str(tarEach[0])
           print "Here I am 3!"
           try:
              recResult = arcpy.ReconcileVersions_management(r"B:\Public\GIS\Service\Database Connections\SDED_SDE.sde",
                                                             "ALL_VERSIONS",
                                                             theTarget,
                                                             preChildList,
                                                             "LOCK_ACQUIRED",
                                                             "NO_ABORT",
                                                             "BY_OBJECT",
                                                             "FAVOR_TARGET_VERSION",
                                                             "NO_POST",
                                                             "KEEP_VERSION",
                                                             preFile)
              if recResult.status == 4:
                 recResStat = recResult.status
                 recResStr = "\Reconcile & Post to " + str(theTarget) + \
                             " succeeded!"
                 print resultStr
           except Exception as e:
              #resultStr = "\n A conflict detected under the version " + theTarget + "\n"
              #resultStr = resultStr +  " because of " +  e.message + "\n"
              #detail = "Conflict detected, Please see the log file ( " + preFile + " ) for details"
              status = "ERROR"
              cCount +=1
              #print "confilct detected  for ", theTarget, e.message
              print "RECONCILE           ERROR", OracleInstance, e.message
              #lines.append(str(resultStr)) 

        ## Run the compress tool. 
        #arcpy.Compress_management(SDEConnection)

        ## Allow the database to begin accepting connections again
        #arcpy.AcceptConnections(SDEConnection, True)

        ## Get a list of datasets owned by the admin user

        ## Rebuild indexes and analyze the states and states_lineages system tables
        #arcpy.RebuildIndexes_management(workspace, "SYSTEM", "ALL")

        #arcpy.AnalyzeDatasets_management(workspace, "SYSTEM", "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")

    except Exception as expt:
       print "Here I am 9"
       print "RECONCILE           ERROR", OracleInstance, expt.message
       #errorStr = "Exception happend: " +  expt.message + "\n"
       #eCount += 1
       #status = "ERROR"
       #detail = "Please see the log file ( " + file + " ) for details"
       #lines.append(str(errorStr))
