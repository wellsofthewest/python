# ===================================================================================
# CustomerExtract.py
# ===================================================================================
# Created by: 		David Speight, True North Geographic Technologies
# Last Modified:	09-26-2013
#
# Description:		This script runs geoprocessing tasks that export
#			geodatabase features from the MTEMC production database
#			into a file geodatabase for vegetation management.
# ===================================================================================

# ===================================================================================
# DEFINE PARAMETERS & OBJECTS
# ===================================================================================
import arcpy
import datetime
import time
import os
import sys
import traceback
startDateTime = time.time()
# ---------------------------------------------------------------------------
# Enable error handling
# ---------------------------------------------------------------------------
def deliverMessage(message):
    currentdatetime = str(datetime.datetime.now())
    logFile.write(currentdatetime + " - " + message + "\n")
    print message
    arcpy.AddMessage(message)

def getError():
    # get the traceback object
    tBack = sys.exc_info()[2]
    # tbinfo contains the line number that the code failed on and the code from that line
    tbinfo = traceback.format_tb(tBack)
    tbStr = ""
    for i in range(0,len(tbinfo)):
        tbStr = tbStr + str(tbinfo[i]) + "\n"
    # write traceback errors to the log file
    deliverMessage(tbStr)
    # generate a message string for any geoprocessing tool errors
    msgs = "Geoprocessing Error Messages:\n" + arcpy.GetMessages(2)
    # Deliver message via the function(s)
    deliverMessage(msgs)
    sys.exit()


# ---------------------------------------------------------------------------
# Set local path variables
# ---------------------------------------------------------------------------
sPath = os.path.normcase(os.path.dirname(sys.argv[0]))
TempGDB = sPath + "\TempWorkspace\CustomerTemp.gdb"
OutGDB = sPath + "\TempWorkspace\CustomerData.gdb"
ProdGDB = "ProdWorkspace\CustomerData.gdb"
TempFolder = sPath + "\TempWorkspace"
LogFolder = sPath + "\LogFiles"


# ---------------------------------------------------------------------------
# Set datasource variables
#	- comment/uncomment appropriate values depending on data source
#	- need to include a workspace path for referencing related tables
# ---------------------------------------------------------------------------

# dev enterprise geodatabase
SourceWorkspace = sPath + "\SourceWorkspace\\MTEMC_DEV.sde\\mtemc_gis.gisadmin."
AddressFolder = sPath + "\AddressSource\MTEMC_Extract.gdb"
#Set Overwrite Parameter
arcpy.env.overwriteOutput = True
# disable qualified field names
arcpy.env.qualifiedFieldNames = "UNQUALIFIED"

# ---------------------------------------------------------------------------
# Set & Open log file
# ---------------------------------------------------------------------------
StartTime = (datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d_%H%M'))
logFile = open(LogFolder + "\\CustomerExtract_" + "log_" + StartTime + ".txt", 'w')

#----------------------------------------------------------------------------
#Log initial parameters
#----------------------------------------------------------------------------

deliverMessage("")
deliverMessage("")
deliverMessage("=========================================================================================================================")
deliverMessage(" CUSTOMER EXTRACT SCRIPT                                     ")
deliverMessage("=========================================================================================================================")
deliverMessage("Started:            " + StartTime)
deliverMessage("Source Workspace:   " + SourceWorkspace)
deliverMessage("Temp GDB:           " + TempGDB)
deliverMessage("Output GDB:         " + OutGDB)
deliverMessage("Log Folder:         " + LogFolder)
deliverMessage("Address Folder:	    " + AddressFolder)
deliverMessage("")
deliverMessage("")

# ---------------------------------------------------------------------------
#   - define spatial reference from dummy shapefile
# ---------------------------------------------------------------------------
descSR = arcpy.Describe(TempFolder + "\\MTEMC_SR.shp")
outputSR = descSR.SpatialReference
arcpy.env.outputCoordinateSystem = outputSR

# ===================================================================================
# EXTRACT DATA & WRITE TO OUTPUT FILES
# ===================================================================================
# ---------------------------------------------------------------------------
# Extract data from enterprise gdb to local temp gdb
# ---------------------------------------------------------------------------

deliverMessage("----Extract data from enterprise gdb to local temp gdb")

try:
    print "CreateTable_management"
    arcpy.CreateTable_management(TempGDB,"ServiceLocation")
except:
    getError()

try:
    print "AddField_management"
    arcpy.AddField_management(TempGDB+"\ServiceLocation","ServiceLocationOID","LONG")
except:
    getError()

try:
    print "AddField_management"
    arcpy.AddField_management(TempGDB+"\ServiceLocation", "DEVICE_LOCATION_ID", "TEXT")
except:
    getError()
print "Search Cursor"
print SourceWorkspace+"ServiceLocation"
tableFC = arcpy.SearchCursor(SourceWorkspace+"ServiceLocation","",outputSR,"","")

print "Search Cursor Created"
tableTemp = arcpy.InsertCursor(TempGDB+"\ServiceLocation")
print "Search Cursor Created"


try:
    for row in tableFC:
         tabRow = tableTemp.newRow()
         tabRow.setValue("ServiceLocationOID", row.getValue("OBJECTID"))
         tabRow.setValue("DEVICE_LOCATION_ID", row.getValue("DEVICE_LOCATION_ID"))
         tableTemp.insertRow(tabRow)
    del row
    del tabRow
except:
    getError()

try:
    arcpy.CreateTable_management(TempGDB,"SP_SL")
except:
    getError()

try:
    arcpy.AddField_management(TempGDB+"\SP_SL", "SP_OID", "LONG")
except:
    getError()

try:
    arcpy.AddField_management(TempGDB+"\SP_SL", "SL_OID", "LONG")
except:
    getError()

try:
    print SourceWorkspace+"SERVICEPOINT_SERVICELOCATION_MVW"
    tableFC = arcpy.SearchCursor(SourceWorkspace+"SERVICEPOINT_SERVICELOCATION_MVW","",outputSR,"","")
    tableTemp = arcpy.InsertCursor(TempGDB+"\SP_SL")
except:
    getError()

try:
    for row in tableFC:
        tabRow = tableTemp.newRow()
        tabRow.setValue("SP_OID", row.getValue("ServicePointObjectID"))
        tabRow.setValue("SL_OID", row.getValue("ServiceLocationObjectID"))
        tableTemp.insertRow(tabRow)
    del row
    del tabRow
except:
    getError()



# ---------------------------------------------------------------
# Multi-table join and export
# ---------------------------------------------------------------
deliverMessage("----Multi-table join and export")
try:
    arcpy.MakeTableView_management(SourceWorkspace+"SAP_ACCOUNT_DATA","SAP_View","",TempGDB)
except:
    getError()

try:
    arcpy.TableToTable_conversion("SAP_View",TempGDB,"SAP")
except:
    getError()

try:
    arcpy.MakeTableView_management(TempGDB+"\SAP","SAP2_View","",TempGDB)
except:
    getError()

try:
    arcpy.MakeTableView_management(TempGDB+"\ServiceLocation","SL_View","",TempGDB)
except:
    getError()

try:
    arcpy.MakeTableView_management(TempGDB+"\SP_SL","SPSL_View","",TempGDB)
except:
    getError()

try:
    arcpy.MakeTableView_management(SourceWorkspace+"ServicePoint","SP_View","",TempGDB)
except:
    getError()

deliverMessage("----Joining relationship class table to location table")
try:
    arcpy.AddIndex_management(TempGDB+"\SP_SL","SL_OID","tmpSLOID","NON_UNIQUE","NON_ASCENDING")
except:
    getError()
try:
    arcpy.AddJoin_management("SL_View","ServiceLocationOID","SPSL_View","SL_OID","KEEP_COMMON")
except:
    getError()
try:
    arcpy.TableToTable_conversion("SL_View",TempGDB,"Locations")
except:
    getError()
# ---------------------------------------------------------------
# Delete unneeded fields from Locations
# ---------------------------------------------------------------
try:
    arcpy.DeleteField_management(TempGDB+"\Locations","ServiceLocationOID; OBJECTID; SL_OID")
except:
    getError()

deliverMessage("----Joining Point Table to Locations Table...")
try:
    arcpy.MakeTableView_management(TempGDB+"\Locations","Location_View", "", TempGDB)
except:
    getError()

try:
    arcpy.AddIndex_management(TempGDB+"\Locations", "SP_OID", "tmpSPOID", "NON_UNIQUE", "NON_ASCENDING")
except:
    getError()

try:
    arcpy.AddJoin_management("Location_View", "SP_OID", "SP_View", "OBJECTID", "KEEP_COMMON")
except:
    getError()

try:
    arcpy.TableToTable_conversion("Location_View", TempGDB, "Points")
except:
    getError()

# ---------------------------------------------------------------
# Delete unneeded fields from Points
# ---------------------------------------------------------------
try:
    arcpy.DeleteField_management(TempGDB + "\Points", "SP_OID; OBJECTID; ANCILLARYROLE; ENABLED; CREATIONUSER; DATECREATED")
except:
    getError()

try:
    arcpy.DeleteField_management(TempGDB + "\Points", "LABELTEXT; DETAIL_INFO; FEEDERID2; CONSTRUCTIONSTATUS")
except:
    getError()

try:
    arcpy.DeleteField_management(TempGDB + "\Points", "WORKORDERID; INSTALLATIONDATE; SYMBOLROTATION; SERVICECURRENTRATING")
except:
    getError()

try:
    arcpy.DeleteField_management(TempGDB + "\Points", "ALTERNATEX; ALTERNATEY; ALTERNATEZ; ALTERNATESOURCE; DATE_INSTALLED")
except:
    getError()

try:
    arcpy.DeleteField_management(TempGDB + "\Points", "STATUS; TYPE; WORKREQUESTID; DESIGNID; WORKFLOWSTATUS; WORKFUNCTION")
except:
    getError()

try:
    arcpy.DeleteField_management(TempGDB + "\Points", "ORIGINALKEY; FOREIGNKEY; GlobalID")
except:
    getError()

deliverMessage(" ----- Joining points to SAP table .....")
try:
    arcpy.MakeTableView_management(TempGDB + "\Points", "Points_View", "", TempGDB)
except:
    getError()

try:
    arcpy.AddIndex_management(TempGDB + "\Points", "DEVICE_LOCATION_ID", "tmpDEVLOCID", "NON_UNIQUE", "NON_ASCENDING")
except:
    getError()

try:
    arcpy.AddIndex_management(TempGDB + "\SAP", "DEV_LOC_NUM", "tmpDEVLOCNUM", "NON_UNIQUE", "NON_ASCENDING")
except:
    getError()

try:
    arcpy.AddJoin_management("SAP2_View", "DEV_LOC_NUM", "Points_View", "DEVICE_LOCATION_ID", "KEEP_COMMON")
except:
    getError()

try:
    arcpy.TableToTable_conversion("SAP2_View", TempGDB, "SAP_Points")
except:
    getError()


# ---------------------------------------------------------------
# Delete unneeded fields
# ---------------------------------------------------------------
try:
    arcpy.DeleteField_management(TempGDB + "\SAP_Points", "DEVICE_LOCATION_ID; Business_Area")
except:
    getError()

# ---------------------------------------------------------------
# Create XY event layer from SAP_Points
# ---------------------------------------------------------------
try:
    arcpy.MakeTableView_management(TempGDB + "\SAP_Points", "SAP_Points_View", "", TempGDB)
except:
    getError()
try:
    arcpy.MakeXYEventLayer_management("SAP_Points_View", "LONG", "LAT", "SAP_Points_Layer", "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];IsHighPrecision")
except:
    getError()

#---------------------------------------------------------------
# Export data to output geodatabase
# ---------------------------------------------------------------
deliverMessage(" ----- Exporting XY data .....")
try:
    arcpy.FeatureClassToFeatureClass_conversion("SAP_Points_Layer",OutGDB,"CustomerPoints")
except:
    getError()

# ---------------------------------------------------------------
# Delete VEG GDB and copy output GDB to VEG server
# ---------------------------------------------------------------
deliverMessage(" ----- Moving results to Clearion folder")
try:
    arcpy.Copy_management(OutGDB,ProdGDB)
except:
    getError()

VEG_CustomerPoints = ProdGDB + "\CustomerPoints"

deliverMessage(" ----- Adding customer address field for Clearion")
# ---------------------------------------------------------------
# Add new field for Clearion -- ADDED 09/26/2013
# ---------------------------------------------------------------
try:
    arcpy.AddField_management(VEG_CustomerPoints, "CUST_ADDR", "TEXT", "", "", "90", "", "NULLABLE", "NON_REQUIRED", "")
except:
    getError()


# ---------------------------------------------------------------
# Calc new field for Clearion -- ADDED 09/26/2013
# ---------------------------------------------------------------
try:
    arcpy.CalculateField_management(VEG_CustomerPoints,"CUST_ADDR","LTrim(RTrim([ADDR_HOUSE_NUM]) + RTrim("" "" + [ADDR_STREET_NAME]) + RTrim("" "" + [ADDR_HOUSE_SUPPL]))", "VB", "")
except:
    getError()

# ===================================================================================
# DELETE CUSTOMER POINT FEATURES IN MTEMC_EXTRACT AND APPEND NEW DATA
# ===================================================================================
deliverMessage(" ----- Updating MTEMC_EXTRACT Customers")

#DEV ENVIRONMENT
SDE_CustomerPoints = sPath+ "\SourceWorkspace\\MTEMC_DEV.sde\\MTEMC_EXTRACT.GISADMIN.CustomerPoints"

# ---------------------------------------------------------------
# Define generic field mapping parameter
# ---------------------------------------------------------------


FieldMap = "DEV_LOC_NUM 'DEV_LOC_NUM' true true false 30 Text 0 0 ,First,#,VEG_CustomerPoints,DEV_LOC_NUM,-1,-1;"
FieldMap = FieldMap + "ACCT_NUM 'ACCT_NUM' true true false 12 Text 0 0 ,First,#,VEG_CustomerPoints,ACCT_NUM,-1,-1;"
FieldMap = FieldMap + "CUST_NAME_FIRST 'CUST_NAME_FIRST' true true false 40 Text 0 0 ,First,#,VEG_CustomerPoints,CUST_NAME_FIRST,-1,-1;"
FieldMap = FieldMap + "CUST_NAME_LAST 'CUST_NAME_LAST' true true false 40 Text 0 0 ,First,#,VEG_CustomerPoints,CUST_NAME_LAST,-1,-1;"
FieldMap = FieldMap + "MTR_NUM_1 'MTR_NUM_1' true true false 18 Text 0 0 ,First,#,VEG_CustomerPoints,MTR_NUM_1,-1,-1;"
FieldMap = FieldMap + "MTR_NUM_2 'MTR_NUM_2' true true false 18 Text 0 0 ,First,#,VEG_CustomerPoints,MTR_NUM_2,-1,-1;"
FieldMap = FieldMap + "MTR_NUM_3 'MTR_NUM_3' true true false 18 Text 0 0 ,First,#,VEG_CustomerPoints,MTR_NUM_3,-1,-1;"
FieldMap = FieldMap + "ADDR_HOUSE_NUM 'ADDR_HOUSE_NUM' true true false 10 Text 0 0 ,First,#,VEG_CustomerPoints,ADDR_HOUSE_NUM,-1,-1;"
FieldMap = FieldMap + "ADDR_STREET_NAME 'ADDR_STREET_NAME' true true false 60 Text 0 0 ,First,#,VEG_CustomerPoints,ADDR_STREET_NAME,-1,-1;"
FieldMap = FieldMap + "ADDR_HOUSE_SUPPL 'ADDR_HOUSE_SUPPL' true true false 10 Text 0 0 ,First,#,VEG_CustomerPoints,ADDR_HOUSE_SUPPL,-1,-1;"
FieldMap = FieldMap + "CITY 'CITY' true true false 40 Text 0 0 ,First,#,VEG_CustomerPoints,CITY,-1,-1;"
FieldMap = FieldMap + "ZIP_CODE 'ZIP_CODE' true true false 10 Text 0 0 ,First,#,VEG_CustomerPoints,ZIP_CODE,-1,-1;"
FieldMap = FieldMap + "STATE 'STATE' true true false 3 Text 0 0 ,First,#,VEG_CustomerPoints,STATE,-1,-1;"
FieldMap = FieldMap + "PHONE_NUM 'PHONE_NUM' true true false 30 Text 0 0 ,First,#,VEG_CustomerPoints,PHONE_NUM,-1,-1;"
FieldMap = FieldMap + "MOBILE_NUM 'MOBILE_NUM' true true false 30 Text 0 0 ,First,#,VEG_CustomerPoints,MOBILE_NUM,-1,-1;"
FieldMap = FieldMap + "GUAR_OF_SUPPLY 'GUAR_OF_SUPPLY' true true false 30 Text 0 0 ,First,#,VEG_CustomerPoints,GUAR_OF_SUPPLY,-1,-1;"
FieldMap = FieldMap + "INSTALL_TYPE 'INSTALL_TYPE' true true false 30 Text 0 0 ,First,#,VEG_CustomerPoints,INSTALL_TYPE,-1,-1;"
FieldMap = FieldMap + "KEY_ACCT 'KEY_ACCT' true true false 4 Text 0 0 ,First,#,VEG_CustomerPoints,KEY_ACCT,-1,-1;"
FieldMap = FieldMap + "BILLING_CLASS 'BILLING_CLASS' true true false 4 Text 0 0 ,First,#,VEG_CustomerPoints,BILLING_CLASS,-1,-1;"
FieldMap = FieldMap + "CONN_OBJ_ID 'CONN_OBJ_ID' true true false 30 Text 0 0 ,First,#,VEG_CustomerPoints,CONN_OBJ_ID,-1,-1;"
FieldMap = FieldMap + "CUST_NAME_TITLE 'CUST_NAME_TITLE' true true false 30 Text 0 0 ,First,#,VEG_CustomerPoints,CUST_NAME_TITLE,-1,-1;"
FieldMap = FieldMap + "CUST_NAME_SUFFIX 'CUST_NAME_SUFFIX' true true false 40 Text 0 0 ,First,#,VEG_CustomerPoints,CUST_NAME_SUFFIX,-1,-1;"
FieldMap = FieldMap + "SUBDIV_NAME 'SUBDIV_NAME' true true false 40 Text 0 0 ,First,#,VEG_CustomerPoints,SUBDIV_NAME,-1,-1;"
FieldMap = FieldMap + "LOT_NUM 'LOT_NUM' true true false 20 Text 0 0 ,First,#,VEG_CustomerPoints,LOT_NUM,-1,-1;"
FieldMap = FieldMap + "ITRON_NOTE_1 'ITRON_NOTE_1' true true false 255 Text 0 0 ,First,#,VEG_CustomerPoints,ITRON_NOTE_1,-1,-1;"
FieldMap = FieldMap + "ITRON_NOTE_2 'ITRON_NOTE_2' true true false 255 Text 0 0 ,First,#,VEG_CustomerPoints,ITRON_NOTE_2,-1,-1;"
FieldMap = FieldMap + "ITRON_NOTE_3 'ITRON_NOTE_3' true true false 255 Text 0 0 ,First,#,VEG_CustomerPoints,ITRON_NOTE_3,-1,-1;"
FieldMap = FieldMap + "ITRON_NOTE_4 'ITRON_NOTE_4' true true false 255 Text 0 0 ,First,#,VEG_CustomerPoints,ITRON_NOTE_4,-1,-1;"
FieldMap = FieldMap + "METER_ROUTE 'METER_ROUTE' true true false 8 Text 0 0 ,First,#,VEG_CustomerPoints,METER_ROUTE,-1,-1;"
FieldMap = FieldMap + "METER_CYCLE 'METER_CYCLE' true true false 8 Text 0 0 ,First,#,VEG_CustomerPoints,METER_CYCLE,-1,-1;"
FieldMap = FieldMap + "CT_PT_IND 'CT_PT_IND' true true false 5 Text 0 0 ,First,#,VEG_CustomerPoints,CT_PT_IND,-1,-1;"
FieldMap = FieldMap + "LEGACY_SML 'LEGACY_SML' true true false 30 Text 0 0 ,First,#,VEG_CustomerPoints,LEGACY_SML,-1,-1;"
FieldMap = FieldMap + "LEGACY_SML2 'LEGACY_SML2' true true false 30 Text 0 0 ,First,#,VEG_CustomerPoints,LEGACY_SML2,-1,-1;"
FieldMap = FieldMap + "DEV_LOC_DESCRIPTION 'DEV_LOC_DESCRIPTION' true true false 40 Text 0 0 ,First,#,VEG_CustomerPoints,DEV_LOC_DESCRIPTION,-1,-1;"
FieldMap = FieldMap + "BP_NUM 'BP_NUM' true true false 10 Text 0 0 ,First,#,VEG_CustomerPoints,BP_NUM,-1,-1;"
FieldMap = FieldMap + "GUAR_OF_SUPPLY_CODE 'GUAR_OF_SUPPLY_CODE' true true false 4 Text 0 0 ,First,#,VEG_CustomerPoints,GUAR_OF_SUPPLY_CODE,-1,-1;"
FieldMap = FieldMap + "INSTALL_TYPE_CODE 'INSTALL_TYPE_CODE' true true false 4 Text 0 0 ,First,#,VEG_CustomerPoints,INSTALL_TYPE_CODE,-1,-1;"
FieldMap = FieldMap + "PHONE_NUM3 'PHONE_NUM3' true true false 30 Text 0 0 ,First,#,VEG_CustomerPoints,PHONE_NUM3,-1,-1;"
FieldMap = FieldMap + "PHONE_NUM4 'PHONE_NUM4' true true false 30 Text 0 0 ,First,#,VEG_CustomerPoints,PHONE_NUM4,-1,-1;"
FieldMap = FieldMap + "PREMISE_TYPE_CODE 'PREMISE_TYPE_CODE' true true false 8 Text 0 0 ,First,#,VEG_CustomerPoints,PREMISE_TYPE_CODE,-1,-1;"
FieldMap = FieldMap + "PREMISE_NUM 'PREMISE_NUM' true true false 10 Text 0 0 ,First,#,VEG_CustomerPoints,PREMISE_NUM,-1,-1;"
FieldMap = FieldMap + "DATEMODIFIED 'Date Modified' true true false 36 Date 0 0 ,First,#,VEG_CustomerPoints,DATEMODIFIED,-1,-1;"
FieldMap = FieldMap + "LASTUSER 'Last User' true true false 50 Text 0 0 ,First,#,VEG_CustomerPoints,LASTUSER,-1,-1;"
FieldMap = FieldMap + "SUBTYPECD 'Subtype' true true false 4 Long 0 10 ,First,#,VEG_CustomerPoints,SUBTYPECD,-1,-1;"
FieldMap = FieldMap + "FEEDERID 'Feeder ID' true true false 20 Text 0 0 ,First,#,VEG_CustomerPoints,FEEDERID,-1,-1;"
FieldMap = FieldMap + "ELECTRICTRACEWEIGHT 'Electric Trace Weight' true true false 4 Long 0 10 ,First,#,VEG_CustomerPoints,ELECTRICTRACEWEIGHT,-1,-1;"
FieldMap = FieldMap + "FEEDERINFO 'Feeder Information' true true false 4 Long 0 10 ,First,#,VEG_CustomerPoints,FEEDERINFO,-1,-1;"
FieldMap = FieldMap + "PHASEDESIGNATION 'Phase Designation' true true false 4 Long 0 10 ,First,#,VEG_CustomerPoints,PHASEDESIGNATION,-1,-1;"
FieldMap = FieldMap + "CONNECTIONTYPE 'Connection Type' true true false 20 Text 0 0 ,First,#,VEG_CustomerPoints,CONNECTIONTYPE,-1,-1;"
FieldMap = FieldMap + "COMMENTS 'COMMENTS' true true false 100 Text 0 0 ,First,#,VEG_CustomerPoints,COMMENTS,-1,-1;"
FieldMap = FieldMap + "KEY_ACCOUNT 'Key Account' true true false 1 Text 0 0 ,First,#,VEG_CustomerPoints,KEY_ACCOUNT,-1,-1;"
FieldMap = FieldMap + "GUARANTEE_OF_SUPPLY 'Guarantee Of Supply' true true false 20 Text 0 0 ,First,#,VEG_CustomerPoints,GUARANTEE_OF_SUPPLY,-1,-1;"
FieldMap = FieldMap + "WORKLOCATIONID 'Work Location ID' true true false 20 Text 0 0 ,First,#,VEG_CustomerPoints,WORKLOCATIONID,-1,-1;"
FieldMap = FieldMap + "ORIGINALKEY 'ORIGINALKEY' true true false 20 Text 0 0 ,First,#,VEG_CustomerPoints,ORIGINALKEY,-1,-1;"
FieldMap = FieldMap + "FOREIGNKEY 'FOREIGNKEY' true true false 20 Text 0 0 ,First,#,VEG_CustomerPoints,FOREIGNKEY,-1,-1;"
FieldMap = FieldMap + "CT_PT_INDICATOR 'CT_PT_INDICATOR' true true false 4 Text 0 0 ,First,#,VEG_CustomerPoints,CT_PT_INDICATOR,-1,-1;"
FieldMap = FieldMap + "ACTIVE 'ACTIVE' true true false 2 Short 0 5 ,First,#,VEG_CustomerPoints,ACTIVE,-1,-1;"
FieldMap = FieldMap + "JOB_NUMBER 'JOB_NUMBER' true true false 50 Text 0 0 ,First,#,VEG_CustomerPoints,JOB_NUMBER,-1,-1;"
FieldMap = FieldMap + "LAT 'LAT' true true false 8 Double 8 38 ,First,#,VEG_CustomerPoints,LAT,-1,-1;"
FieldMap = FieldMap + "LONG 'LONG' true true false 8 Double 8 38 ,First,#,VEG_CustomerPoints,LONG,-1,-1;"
FieldMap = FieldMap + "CUST_ADDR 'CUST_ADDR' true true false 90 Text 0 0 ,First,#,VEG_CustomerPoints,CUST_ADDR,-1,-1;"
FieldMap = FieldMap + "GPS 'GPS' true true false 15 Text 0 0 ,First,#,VEG_CustomerPoints,GPS,-1,-1;"
FieldMap = FieldMap + "Meter_Installation_Date 'Meter Installation Date' true true false 36 Date 0 0 ,First,#,VEG_CustomerPoints,Meter_Installation_Date,-1,-1;"
FieldMap = FieldMap + "Device_Category 'Device Category' true true false 12 Text 0 0 ,First,#,VEG_CustomerPoints,Device_Category,-1,-1;"
FieldMap = FieldMap + "CUST_NAME_FULL 'Fullname' true true false 50 Text 0 0 ,First,#,VEG_CustomerPoints,CUST_NAME_FULL,-1,-1"

#print FieldMap
# ----------------------------------------------------------------------------------
# Replace placeholder text in field mapping string with physical path to source data
# ----------------------------------------------------------------------------------
FieldMap = str(FieldMap).replace("VEG_CustomerPoints",VEG_CustomerPoints)

# ---------------------------------------------------------------
# Delete existing point features
# ---------------------------------------------------------------
try:
    arcpy.DeleteFeatures_management(SDE_CustomerPoints)
except:
    getError()

# ---------------------------------------------------------------
# Append new point features from file gdb
# ---------------------------------------------------------------

#Added by TNGEO############################################

# Get the grid sizes from the tool, this is a string with 3 semi-colon seperated values (typically something like "1500; 0; 0") 
result = arcpy.CalculateDefaultGridIndex_management(VEG_CustomerPoints)
indexGrids = []
for count in range(0, result.outputCount):
  print str(count) +" - "+result.getOutput(count)
  indexGrids.append(result.getOutput(count))

# First remove the existing grid index
try:
  print "remove existing grid index"
  arcpy.RemoveSpatialIndex_management(VEG_CustomerPoints)
except:
  print "no index exists"
  # if no index exists, RemoveSpaitalIndex will fail, but just keep going
  pass

# Now add the indexes calculated by the tool
try:
    print "adding spatial index"
    arcpy.AddSpatialIndex_management(VEG_CustomerPoints, indexGrids)
except:
    print "cannot add spatialIndex"
    pass
#END Added by TNGEO############################################

  
try:
    print "appending Veg_Customer Points"
    arcpy.Append_management(VEG_CustomerPoints,SDE_CustomerPoints,"NO_TEST",FieldMap,"")
except:
    print "error on appending VegCustomerPoints to SDE CustomerPoints"
    tBack = sys.exc_info()[2]
    # tbinfo contains the line number that the code failed on and the code from that line
    tbinfo = traceback.format_tb(tBack)
    tbStr = ""
    for i in range(0,len(tbinfo)):
        tbStr = tbStr + str(tbinfo[i]) + "\n"
    # write traceback errors to the log file
    print tbStr
    # generate a message string for any geoprocessing tool errors
    msgs = "Geoprocessing Error Messages:\n" + arcpy.GetMessages(2)
    # Deliver message via the function(s)
    print msgs
    #pass
    #getError()


# ---------------------------------------------------------------------------
# Delete old GenerationPartners feature class and Export New CustomerPoints feature class
# ---------------------------------------------------------------------------
deliverMessage(" ----- Exporting new CustomerPoints feature class to AddressSource\MTEMC_Extract.gdb")

Current_Customers = AddressFolder + "\CustomerPoints"
#Delete old CustomerPoints feature class
try:
    arcpy.DeleteFeatures_management(Current_Customers)
except:
    getError()

#Add new CustomerPoints feature class points to Serverbase\AddressSource\MTEMC_Extract.gdb
try:
    arcpy.Append_management(OutGDB+"\CustomerPoints",Current_Customers,"NO_TEST",FieldMap,"")
except:
    #pass
    getError()

# ===================================================================================
# FINISH & CLEAN UP
# ===================================================================================
endDateTime = time.time()
deliverMessage("")
deliverMessage("")
deliverMessage("=========================================================================================================================")
deliverMessage(" SCRIPT COMPLETED -----  {:.2f} minutes".format((endDateTime - startDateTime) / 60))
deliverMessage("=========================================================================================================================")
try:
    now = time.time()
    cutoff = now - (2*60)

    files = os.listdir(LogFolder)
    for file in files:
        ext = os.path.splitext(file)[-1].lower()
        if os.path.isfile(LogFolder+"//"+file):
            t = os.stat(LogFolder+"//"+file)
            c = t.st_ctime
            if c < cutoff:
                if ext == ".log":
                    os.remove(LogFolder+"//"+file)
except:
    getError()
    #logEvent(2,"GENERIC METERS: Trim Log Files Failed")
