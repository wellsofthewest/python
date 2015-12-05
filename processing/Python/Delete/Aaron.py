# Author:  Tim Anderson, Barr Engineering Company
# Update Date:    October 7, 2015
# Version: ArcGIS 10.3
# Purpose:
# Assumptions:
#       Dig locations are reprojected into same coordinate system as data
#       This version was written so that Spatial Analyst and Advanced License are not required
#       All raster data must be converted to vector format before utilizing this script

import arcpy
from arcpy import env

import sys, string, os, arcgisscripting
import platform
import datetime


#List data locations
Action_Areas_FC = r"C:\Users\kati7527\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\DSCREATOR.sde\C_Magellan_EnviroTool.DSCREATOR.ActionAreas"
#Action_Areas_FC2 = "Database Connections\\Connection to T_Locking_DSCREATOR.sde\\T_Locking.DSCREATOR.ActionArea"
States_FC = r"C:\Users\kati7527\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\DSCREATOR.sde\C_Magellan_EnviroTool.DSCREATOR.States"
theAnalysisParam_Table = r"C:\Users\kati7527\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\DSCREATOR.sde\C_Magellan_EnviroTool.DSCREATOR.DataAnalysis_Table"
Magellan_ReviewData = r"C:\Users\kati7527\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\DSCREATOR.sde\C_Magellan_EnviroTool.DSCREATOR.US_Review_Data"
Release_Locations_FC = r"C:\Users\kati7527\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\DSCREATOR.sde\C_Magellan_EnviroTool.DSCREATOR.Release_Locations"
#theWorkSpace = "C:\Users\kati7527\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\DSCREATOR.sde"
#theWorkSpace = "Database Connections\\Connection to T_Locking_DSCREATOR.sde"

GroupIDFld = "Group_ID"
UniqueSiteIDFld = "Unique_ID"

arcpy.env.overwriteOutput = 1


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False



def FieldExist(featureclass, fieldname):
    fieldList = arcpy.ListFields(featureclass, fieldname)

    fieldCount = len(fieldList)

    if (fieldCount == 1):
        return True
    else:
        return False

def Point_Review_Data(ReviewDataFC, UniqueID, thePolygon, MaxOffset,Param_Table,datetext):

    #This subroutine will first perform a select by distance from the action area polygon the full amount (MaxOffset, in feet).  If the buffer does not intersect the
    #feature class, the subroutine will return a -999 value.

    #Create a dictionary to return values.  The "key" will the field name in the action area table the value is to written.
    #the item for each key will be the value that will be written back to the respective field in the action area table
    theResultPntDict = {}
    #Analyze "within polygon" types first
    TypeFld = arcpy.AddFieldDelimiters(Param_Table, "Analysis_Type")

    theQuery = TypeFld + " = 'Point Within Polygon with Attribute'"
    theDataList = arcpy.SearchCursor(Param_Table,theQuery)

    for theData in theDataList:
        TheCheckField = theData.getValue("Magellan_FieldName")
        AnalysisName = theData.getValue("UniqueID")
        theExtent = theData.getValue("AnalysisArea")
        AA_ReportFld1 = theData.getValue("ActionArea_FieldName1")
        AA_ReportFld2 = theData.getValue("ActionArea_FieldName2")
        CheckValues1 = theData.getValue("Value1")
        theFieldListTemp = theData.getValue("Value2")
        theFieldList = theFieldListTemp.split(",")

        #if There are no features inside of 2X buffer, return distance value -999 and "None" in attribute field
        BufferUnits = str(MaxOffset*2.0) + " Feet"
        PointsLayer = "Point_lyr"
        arcpy.MakeFeatureLayer_management(ReviewDataFC, PointsLayer)
        arcpy.SelectLayerByLocation_management (PointsLayer, "INTERSECT", thePolygon, BufferUnits)
        matchcount = int(arcpy.GetCount_management(PointsLayer)[0])

        if matchcount == 0:

            theResultPntDict[AA_ReportFld2] = "None,None,None"
            theResultPntDict[AA_ReportFld1] = "-999"

        else:
            #There are points within the 2x buffer.  Create a temporary data feature class from the selection set
            SelectFeat_in_2xBuffer_FC = "SelectdFeaturesTemp_" + datetext
            arcpy.CopyFeatures_management(PointsLayer, SelectFeat_in_2xBuffer_FC)
            shapeName = arcpy.Describe(SelectFeat_in_2xBuffer_FC).shapeFieldName
            theFeatList = arcpy.SearchCursor(SelectFeat_in_2xBuffer_FC)

            TextDistDict = {}
            for Feat in theFeatList:
                ptGeometry = Feat.getValue(shapeName)

                #ptGeometry = arcpy.PointGeometry(thePoint)
                theDistance = ptGeometry.distanceTo(thePolygon)
                #the data units are in meters so must convert to Feet
                theDistance = int(theDistance/0.3048)
                theText = ""
                thecnt = 0
                NumFlds = len(theFieldList)
                for fld in theFieldList:
                    thecnt = thecnt + 1
                    if str(fld) == "Rel_Date":
                        theFldValue = str(Feat.getValue(fld))
                    else:
                        theFldValue = Feat.getValue(fld)
                    if thecnt < NumFlds:
                        theText = theText + theFldValue + ","
                    else:
                        theText = theText + theFldValue

                TextDistDict[theText] = theDistance

            theKeys =  TextDistDict.keys()
            Fld1_Value = ""
            Fld2_Value = ""
            theCnt = 0
            NumVals = len(theKeys)
            for val in theKeys:
                theCnt = theCnt + 1
                theDist = TextDistDict[val]
                if theCnt < NumVals:
                    Fld1_Value = Fld1_Value + val + "$$$"
                    Fld2_Value = Fld2_Value + str(theDist) + "$$$"
                else:
                    Fld1_Value = Fld1_Value + val
                    Fld2_Value = Fld2_Value + str(theDist)

            theResultPntDict[AA_ReportFld2] = Fld1_Value
            theResultPntDict[AA_ReportFld1] = Fld2_Value

    arcpy.Delete_management(PointsLayer)
    return theResultPntDict




def Polygon_Review_Data(ReviewDataFC, UniqueID, thePolygon, MaxOffset,Param_Table,datetext):

    #This subroutine will first perform a select by distance from the action area polygon the full amount (MaxOffset, in feet).  If the buffer does not intersect the
    #feature class, the subroutine will return a -999 value.
    #

    #Clip state review data to 2 x buffer distance
    spatial_ref = arcpy.Describe(ReviewDataFC).spatialReference

    theBufferX2 = "FeatureBufferX2"
    try:
        BufferX2 = MaxOffset * 2.0
        BufferUnits = str(BufferX2) + " Feet"
        arcpy.Buffer_analysis (thePolygon, theBufferX2, BufferUnits)
    except:
        arcpy.AddError("Error in buffering x 2")
        sys.exit()

    RevDataInBufferX2 = os.path.join(arcpy.env.scratchGDB, "ReviewDataInBufferX2_" + UniqueID)
    try:
        arcpy.Clip_analysis (ReviewDataFC, theBufferX2, RevDataInBufferX2)
    except:
        arcpy.AddError("Error in clipping to buffer x 2")
        sys.exit()

    #Clip state review data to buffer distance

    theBuffer = "FeatureBuffer"
    BufferUnits = str(MaxOffset) + " Feet"
    try:
        arcpy.Buffer_analysis (thePolygon, theBuffer, BufferUnits)
    except:
        arcpy.AddError("Error in buffering (state data)")
        sys.exit()


    RevDataInBuffer = os.path.join(arcpy.env.scratchGDB, "ReviewDataInBuffer_" + UniqueID)
    try:
        arcpy.Clip_analysis (RevDataInBufferX2, theBuffer, RevDataInBuffer)
    except:
        arcpy.AddError("Error in clipping to buffer (state data)")
        sys.exit()



    #Clip state review data to action area
    RevDataInActionArea = os.path.join(arcpy.env.scratchGDB, "ClippedReviewData_" + UniqueID)
    try:
        arcpy.Clip_analysis (RevDataInBuffer, thePolygon, RevDataInActionArea)
    except:
        arcpy.AddError("Error in clipping to action area")
        sys.exit()

    #Create a dictionary to return values.  The "key" will the field name in the action area table the value is to written.
    #the item for each key will be the value that will be written back to the respective field in the action area table
    theResultDict = {}

    #Analyze "within polygon" types first
    TypeFld = arcpy.AddFieldDelimiters(Param_Table, "Analysis_Type")

    theQuery = TypeFld + " = 'Within Polygon' OR " + TypeFld + " = 'Within Polygon with Attribute'"
    theDataList = arcpy.SearchCursor(Param_Table,theQuery)

    for theData in theDataList:
        TheCheckField = theData.getValue("Magellan_FieldName")
        AnalysisName = theData.getValue("UniqueID")
        theExtent = theData.getValue("AnalysisArea")
        AA_ReportFld = theData.getValue("ActionArea_FieldName1")
        CheckValues = theData.getValue("Value1")
        AnalysisType = theData.getValue(TypeFld)

        #CheckValues from Value1 field should be a string with two comma seperated values.  The first value indicates what result to summarize if true, second
        #value is result to provide if false (no data is found)
        theParts = CheckValues.split(",")
        ifFound    = theParts[0]
        ifNotFound = theParts[1]

        if theExtent == "Action Area":
            AnalysisData = RevDataInActionArea
        elif theExtent == "Buffer":
            AnalysisData = RevDataInBuffer
        elif theExtent == "2XBuffer":
            AnalysisData = RevDataInBufferX2
        else:
            arcpy.AddError("Analysis Area type is invalid:  " +theExtent)
            sys.exit()

        QueryFld = arcpy.AddFieldDelimiters(AnalysisData,TheCheckField)

        theValueQuery = QueryFld + " <> ''"
        #arcpy.AddMessage(theValueQuery)
        theAreaRecs = arcpy.SearchCursor(AnalysisData,theValueQuery)
        theValues = []  #List of values in field
        cnt = 0
        for recs in theAreaRecs:
            cnt = cnt + 1
            theValue = recs.getValue(TheCheckField)
            if theValue is not None:
                theValues.append(theValue)
        if cnt > 0:
            del recs
        del theAreaRecs

        if AnalysisType == 'Within Polygon':
            if cnt == 0:
                theOutput = ifNotFound
            else:
                theOutput = ifFound

        else:  #summarize attributes within analysis area, if no values, specify "None"
            theValues = list(set(theValues))
            if len(theValues) > 0:
                theOutput = ""
                theCount = -1
                for theVal in theValues:
                    theCount = theCount + 1
                    if theCount > 0:
                        theOutput = theOutput + "$$$" + theVal
                    else:
                        theOutput = theOutput + theVal
            else:
                theOutput = ifNotFound


        theResultDict[AA_ReportFld] = theOutput
    del theData
    del theDataList

#   Now perform analysis on features where percent of total is required (currently only NLCD)

    theQuery = TypeFld + " = 'Percent'"
    theDataList = arcpy.SearchCursor(Param_Table,theQuery)

    for theData in theDataList:
        TheCheckField = theData.getValue("Magellan_FieldName")
        AnalysisName = theData.getValue("UniqueID")
        theExtent = theData.getValue("AnalysisArea")
        AA_ReportFld = theData.getValue("ActionArea_FieldName1")
        CheckValues = theData.getValue("Value1")
        PercentNum = theData.getValue("Percent_")
        PercentVal = theData.getValue("PercValues")

        #CheckValues from Value1 field should be a string with two comma seperated values.  The first value indicates what result to summarize if true, second
        #value is result to provide if false (no data is found)
        theParts = CheckValues.split(",")
        ifFound    = theParts[0]
        ifNotFound = theParts[1]


        if theExtent == "Action Area":
            AnalysisData = RevDataInActionArea
        elif theExtent == "Buffer":
            AnalysisData = RevDataInBuffer
        elif theExtent == "2XBuffer":
            AnalysisData = RevDataInBufferX2
        else:
            arcpy.AddError("AnalysisArea type is invalid:  " +theExtent)
            sys.exit()

        desc = arcpy.Describe(AnalysisData)
        AreaField = desc.areaFieldName

        #Loop through all records in the clipped data for the specified extent
        TotalArea = 0.0
        FoundArea = 0.0
        theRecs = arcpy.SearchCursor(AnalysisData)
        for rec in theRecs:
            theArea = rec.getValue(AreaField)
            theFldValue = rec.getValue(TheCheckField)
            TotalArea = TotalArea + theArea
            if theFldValue == PercentVal:
                FoundArea = FoundArea + theArea

        if TotalArea == 0.0:
           arcpy.AddError("Extent Total equals zero.")
           sys.exit()
        else:
            Percentage = FoundArea/TotalArea


        if Percentage >= PercentNum:
            theOutput = ifFound
        else:
            theOutput = ifNotFound


        theResultDict[AA_ReportFld] = theOutput

        del rec
        del theRecs

#   Now perform analysis on features where distance calculation is required

    theQuery = TypeFld + " = 'Distance with Attribute'"
    theDataList = arcpy.SearchCursor(Param_Table,theQuery)
    for theData in theDataList:
        TheCheckField = theData.getValue("Magellan_FieldName")
        AnalysisName = theData.getValue("UniqueID")
        theExtent = theData.getValue("AnalysisArea")
        AA_ReportFld = theData.getValue("ActionArea_FieldName1")
        AA_ReportFld2 = theData.getValue("ActionArea_FieldName2")
        CheckValues = theData.getValue("Value1")

        #if There are no features inside of 2X buffer, return distance value -999 and "None" in attribute field

        if theExtent == "Action Area":
            AnalysisData = RevDataInActionArea
        elif theExtent == "Buffer":
            AnalysisData = RevDataInBuffer
        elif theExtent == "2XBuffer":
            AnalysisData = RevDataInBufferX2
        else:
            arcpy.AddError("AnalysisArea type is invalid:  " +theExtent)
            sys.exit()


        desc = arcpy.Describe(AnalysisData)
        theExtentRecs = arcpy.SearchCursor(AnalysisData)
        ValidTypes = []

        QueryFld = arcpy.AddFieldDelimiters(AnalysisData,TheCheckField)
        theQuery = QueryFld + " <> ''"

        ExtentLayer2 = "extent2_lyr"
        arcpy.MakeFeatureLayer_management (AnalysisData, ExtentLayer2)
        arcpy.SelectLayerByAttribute_management (ExtentLayer2, "NEW_SELECTION", theQuery)
        matchcount = int(arcpy.GetCount_management(ExtentLayer2)[0])
	arcpy.Delete_management(ExtentLayer2)
        if matchcount == 0:
            #there are no features with attributes within the 2x buffer area
            theDistance = -999.0
            theType = "None"

        else:   #check to see if there area features within the action area
            ExtentLayer = "extent_lyr"
            arcpy.MakeFeatureLayer_management (RevDataInActionArea, ExtentLayer)
            arcpy.SelectLayerByAttribute_management (ExtentLayer, "NEW_SELECTION", theQuery)
            matchcount = int(arcpy.GetCount_management(ExtentLayer)[0])
            if matchcount > 0:
                #Create a temporary data feature class from the selection set
                SelectFeat_in_AA_FC = "SelectdFeaturesTemp_" + datetext
                arcpy.CopyFeatures_management(ExtentLayer, SelectFeat_in_AA_FC)
                theTypes = []
                theFeatList = arcpy.SearchCursor(SelectFeat_in_AA_FC)
                for Feat in theFeatList:
                    theValue = Feat.getValue(TheCheckField)
                    theTypes.append(theValue)

                theTypes = list(set(theTypes))
                theType= theTypes[0]
                theDistance = 0.0

            else:  #there is at least one feature between the Action area and 2x buffer distance, look at distance between Action area and all features
                   #Look at all features to see which is closest to action area.
                QueryFld = arcpy.AddFieldDelimiters(AnalysisData,TheCheckField)
                theQuery = QueryFld + " <> ''"
                #the2XFeatures = arcpy.da.SearchCursor(RevDataInBufferX2,['SHAPE@',TheCheckField],theQuery)
                the2XFeatures = arcpy.SearchCursor(RevDataInBufferX2,theQuery)
                shapeName = arcpy.Describe(RevDataInBufferX2).shapeFieldName
                MinDistance = 999999999999.0
                Numfeat = 0
                for feat in the2XFeatures:

                    Numfeat = Numfeat + 1
                    thefeatpoly = feat.getValue(shapeName)
                    theType1 = feat.getValue(TheCheckField)
                    NumParts = thePolygon.partCount
                    if NumParts > 1:
                        arcpy.AddError("Number of parts  > 1 in action area polygon")
                        sys.exit()


                    thePart = thefeatpoly.getPart(0)
                    theFeatPoly = arcpy.Geometry("polygon",thePart,spatial_ref)
                    theAAPart = thePolygon.getPart(0)
                    theAAPoly = arcpy.Geometry("polygon",theAAPart,spatial_ref)
                    theDistance =  theFeatPoly.distanceTo(theAAPoly)
                    #the data units are in meters so must convert to Feet
                    theDistance = int(theDistance/0.3048)
                    #arcpy.AddMessage ("thedistance = "+  str(theDistance))
                    if theDistance < MinDistance:
                        MinDistance = theDistance
                        theType = theType1

                theDistance = MinDistance
                arcpy.Delete_management(ExtentLayer)



        #arcpy.AddMessage("TheDistance = " + str(theDistance))
        #arcpy.AddMessage("TheType =  " + theType)
        theResultDict[AA_ReportFld] = theType
        theResultDict[AA_ReportFld2] = theDistance
    del theData
    del theDataList
    return theResultDict



#The group ID is passed to the script.  This ID represents the Action Areas where analysis is requested.
GroupID = "Tim" #arcpy.GetParameterAsText(0)
theBufferText = 200 #arcpy.GetParameterAsText(1)
theBuffer = float(theBufferText)


#get current time to use for appending to filenames

rightnow1 = datetime.datetime.now()
rightnow = "X" + str(rightnow1.strftime("%Y%m%d%H%M%S"))
##
arcpy.env.workspace = r"C:\Temp\copied.gdb"

# Get the shape type  of the input Action Area feature class


desc = arcpy.Describe(Action_Areas_FC)
type = desc.shapeType
if type != "Polygon":
  arcpy.AddError("Input must be polygon!")
  sys.exit()


#Loop through input Action Area Polygons

theCount = 0
GroupIDFld = "Group_ID"
UniqueSiteIDFld = "Unique_ID"
Datefld = "Analysis_Date"
Grpfld = arcpy.AddFieldDelimiters(Action_Areas_FC, GroupIDFld)
UIDfld = arcpy.AddFieldDelimiters(Action_Areas_FC, UniqueSiteIDFld)
GrpDateFld = arcpy.AddFieldDelimiters(Action_Areas_FC, Datefld)
##
##
theQuery = Grpfld + " = " + "'" + GroupID + "'"

theRows = arcpy.UpdateCursor(Action_Areas_FC,theQuery)
#Get number of values to analyze
DigCount = 0
for dig in theRows:
    DigCount = DigCount + 1

theRows = arcpy.UpdateCursor(Action_Areas_FC,theQuery)

#Check to see if there is at least one record in the selection set
arcpy.AddMessage("Number of sites to analyze assuming all dates = " + str(DigCount))
if DigCount < 1:
    arcpy.AddError("There are no features with GroupID = " + GroupID)
    sys.exit()
else:
    del dig

UniqueDates = []
for row in theRows:
    theDate = row.getValue(Datefld)
    UniqueDates.append(theDate)

del row
del theRows
##
UniqueDates = list(set(UniqueDates))
UniqueDates.sort()
UseDate = UniqueDates[0]

NumDates = len(UniqueDates)
arcpy.AddMessage("numdates = " + str(NumDates))
arcpy.AddMessage("Date = " + str(UseDate))

the2ndQuery = "(" + GroupIDFld + " = '" + GroupID + "') and (" + GrpDateFld + " = '" + str(UseDate) + "')"
#arcpy.AddMessage("2nd Query = " + the2ndQuery)
theRows = arcpy.UpdateCursor(Action_Areas_FC,the2ndQuery)
DigCount = 0
UniqueIDVals = []
for dig in theRows:
    DigCount = DigCount + 1
    theVal = dig.getValue(UniqueSiteIDFld)
    UniqueIDVals.append(theVal)

if DigCount < 1:
    arcpy.AddError("There are no features with GroupID = " + GroupID + " with date = " + UseDate)
    sys.exit()
else:
    del dig
del theRows


theFieldsDict = {}
#Create and populate dictionary with field names and order
theFieldsDict[GroupIDFld] = 1
theFieldsDict[UniqueSiteIDFld] = 2
theFieldsDict["NWI_Type"] = 3
theFieldsDict["NativeVegPer"] = 4
theFieldsDict["Release"] = 5
theFieldsDict["HydricSoil"] = 6
theFieldsDict["ExclusionPeriod"] = 7
theFieldsDict["PublicLand"] = 8
theFieldsDict["Restrictions"] = 9
theFieldsDict["Restrictions1"] = 10
theFieldsDict["Species"] = 11
theFieldsDict["FEMA"] = 12
theFieldsDict["NHD_Type"] = 13
theFieldsDict["NWI_Distance"] = 14
theFieldsDict["ReleaseInfo"] = 15

theFields = ["SHAPE@"]
theFldKeys = theFieldsDict.keys()
theFields.extend(theFldKeys)
layer_name = "AALayer"



arcpy.MakeFeatureLayer_management(Action_Areas_FC, layer_name)
for theVal in UniqueIDVals:
    arcpy.AddMessage("CALCULATING VALUES FOR UNIQUEID = " + str(theVal))

    the3rdQuery = "(" + GroupIDFld + " = '" + GroupID + "') and (" + GrpDateFld + " = '" + str(UseDate) + "') and ("+ UniqueSiteIDFld + " = '" + theVal + "')"
    #arcpy.AddMessage("query = " + the3rdQuery)

    arcpy.SelectLayerByAttribute_management(layer_name, 'NEW_SELECTION',the3rdQuery)
    SelectFeature_FC = rightnow
    arcpy.CopyFeatures_management(layer_name, SelectFeature_FC)

    theFeatList = arcpy.SearchCursor(SelectFeature_FC)
    shapeName = arcpy.Describe(SelectFeature_FC).shapeFieldName
    icount = 0
    for theSite in theFeatList:
        icount = icount + 1
        thePolygon = theSite.getValue(shapeName)
    if icount <> 1:
        arcpy.AddError("There can only be ONE feature with unique ID = " + theVal + ".  Number found = " + str(icount))
        sys.exit()
    del theSite
    del theFeatList

    #Call function that calculates values.  Returns a dictionary with fieldname as key, with repective values.
    thePolygonResultDic = Polygon_Review_Data(Magellan_ReviewData, str(theVal),thePolygon, theBuffer,theAnalysisParam_Table,rightnow)
    theKeys = thePolygonResultDic.keys()

    #Call function that calculates point values.  Returns a dictionary with fieldname as key, with repective values.)
    arcpy.AddMessage("Running point analysis")
    thePointResultDic = Point_Review_Data(Release_Locations_FC, str(theVal),thePolygon, theBuffer,theAnalysisParam_Table,rightnow)
    theKeys2 = thePointResultDic.keys()

    for fld2 in theKeys2:
            #arcpy.AddMessage("calculating value for field:  " + fld2)

            arcpy.CalculateField_management(layer_name, fld2, "'"+thePointResultDic[fld2]+"'", 'PYTHON')


    for fld in theKeys:
            #arcpy.AddMessage("calculating value for field:  " + fld)


            if fld == "NWI_Distance":
                arcpy.CalculateField_management(layer_name, fld, thePolygonResultDic[fld], 'PYTHON')
            else:
                arcpy.CalculateField_management(layer_name, fld, "'" + thePolygonResultDic[fld]+"'", 'PYTHON')


##    except arcpy.ExecuteError:
##        ArcPy.AddError(arcpy.GetMessages(2))

arcpy.Delete_management(layer_name)
arcpy.SetParameter(1, "Message of some sort")

arcpy.AddMessage("Done")



