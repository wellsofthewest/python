import sys, string, os, arcpy, time, cx_Oracle
arcpy.env.parallelProcessingFactor = "100%"
arcpy.env.autoCommit = 7500
arcpy.SetLogHistory(False)
arcpy.scratchWorkspace = "in_memory\\Results"
#
# Local variables...
#
# The next line is used for testing. This only selects one polygon ...
# 41 seconds  
#
v_CwmpWhere = "OBJECTID = '26167'"
#
# Use the next line to the search all polygons ...
#
#v_CwmpWhere = "PLAN_MAP_SYMBOL = 'RH'"
v_Distance = "-3.0 Feet"
v_Parcels = r"\\pao2k\dfsroot\MapService\Database Connections\Paogisdb4\Default\paoread.sde\PAO.Land\PAO.Parcels"
v_Cwmp = r"\\pao2k\dfsroot\MapService\Database Connections\Paogisdb4\Default\paoread.sde\PAO.Ppc\PAO.Countywide_Plan_Map_Categories"
v_ParcelsLayer = "PARCELS_LAYER"
v_CwmpLayer = "CWMP_LAYER"
v_TotalSelected = 0
v_SubTotal = 0
v_String = ""

print "Start at " + str(time.asctime( time.localtime(time.time()) ))

connection = cx_Oracle.connect('paoread', 'paoread1.', 'paoprodgis2:1532/paogisdb4.paoprodgis2.pao2k.co.pinellas.fl.us')
cursor = connection.cursor()
#
# Make the parcel Feature Layer (a pointer to the feature class) ...
#
arcpy.MakeFeatureLayer_management(v_Parcels, v_ParcelsLayer, "", "", "")
#
# Make the Countywide Map Plan Feature Layer (a pointer to the feature class) ...
#
arcpy.MakeFeatureLayer_management(v_Cwmp, v_CwmpLayer, "", "", "")
#
# Select Layer By Attribute for the Countywide Map Plan ...  
#
arcpy.SelectLayerByAttribute_management(v_CwmpLayer, "NEW_SELECTION", v_CwmpWhere)
#
# Loop through the Countywide Map polygon ...
#
with arcpy.da.SearchCursor(v_CwmpLayer, ['OBJECTID','PLAN_MAP_SYMBOL', 'PLAN_MAP_CATEGORY', 'LAST_EDITED_DATE'], "") as v_CwmpCursor:
  for v_CwmpRow in v_CwmpCursor:
    print "Processing CWMP " + str(v_CwmpRow[0]) + " " + v_CwmpRow[1]
    #
    # Select Layer By Attribute for the Countywide Map Plan ...  
    #
    arcpy.SelectLayerByAttribute_management(v_CwmpLayer, "NEW_SELECTION", "OBJECTID = " + str(v_CwmpRow[0]))    
    #
    # Select the Parcels within CWMP polygon ...
    #
    arcpy.SelectLayerByLocation_management(v_ParcelsLayer, "INTERSECT", v_CwmpLayer, "", "NEW_SELECTION")    
    #
    # Get the parcels within this CWMP ...
    #
    with arcpy.da.SearchCursor(v_ParcelsLayer, ['PIN',"SHAPE@XY"], "") as v_ParcelsCursor:
      for v_ParcelRow in v_ParcelsCursor:
        v_CoordX, v_CoordY = v_ParcelRow[1]
        print "    Strap " + v_ParcelRow[0] + " Located at (" + str(int(round(v_CoordX))) +\
              ", " + str(int(round(v_CoordY))) + ")"    
        #
        # Oracle insert ...
        #
        v_InsertSql = \
          "INSERT  /*+ APPEND */ INTO paoread.cwmp_parcels (strap, plan_map_symbol, plan_map_category, pt_centroid_x, " +\
             "pt_centroid_y, last_edited_date, load_date) " +\
          "VALUES (:1, :2, :3, :4, :5, :6, SYSDATE)"
        v_BindVars = {'1': v_ParcelRow[0], '2': v_CwmpRow[1], '3': v_CwmpRow[2], '4': v_CoordX, '5': v_CoordY, '6': v_CwmpRow[3]}
        #cursor.execute(v_InsertSql, v_BindVars)
        connection.commit()
  
        v_SubTotal += 1
        v_TotalSelected += 1
      
      print "    Selected Parcels for this CWMP " + str(v_SubTotal)
      v_SubTotal = 0

print "Total Selected Parcels =" + str(v_TotalSelected)
print "Finish at " + str(time.asctime( time.localtime(time.time()) ))      

connection.close()