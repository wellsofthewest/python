#-------------------------------------------------------------------------------
# Name:        Create lines between closest points
# Purpose:
# This tool is designed to take two point files with matching coordinate systems
# find the nearest point and draw a line between the two points. Any changes are
# welcome to make the script more streamlined or add additional features
#
# Author:      Christian Wells
#-------------------------------------------------------------------------------

import arcpy, os, math
arcpy.env.overwriteOutput=True

#Tool Parameters

#Point locations where feature will start
#[Feature Layer]
fromPnt = arcpy.GetParameterAsText(0)
#Point locations where feature will end
#[Feature Layer]
toPnt = arcpy.GetParameterAsText(1)
#Output folder location (name and type are predetermined)
#[Folder]
output = arcpy.GetParameterAsText(2)
#Coordinate System of the two features (must match)
#[Coordinate System]
coordSystem = arcpy.GetParameterAsText(3)

#Lists of XY Point Coordinates
fromPntX =[]
fromPntY =[]

toPntX =[]
toPntY =[]

#Feature input search cursor setup
fromCursor = arcpy.SearchCursor(fromPnt)
toCursor = arcpy.SearchCursor(toPnt)

#Create table and add fields
#Table output insert cursor setup
table = os.path.join(output, "Near_Points")
arcpy.CreateTable_management(output, "Near_Points")
arcpy.AddField_management(table, "Start_X", "DOUBLE")
arcpy.AddField_management(table, "Start_Y", "DOUBLE")
arcpy.AddField_management(table, "End_X", "DOUBLE")
arcpy.AddField_management(table, "End_Y", "DOUBLE")
tableCursor = arcpy.InsertCursor(table)

#Add XY fields to the From/To feature classes
arcpy.AddXY_management(fromPnt)
arcpy.AddXY_management(toPnt)

#Get values From Points
for row in fromCursor:
    X = row.getValue("POINT_X")
    Y = row.getValue("POINT_Y")
    fromPntX.append(X)
    fromPntY.append(Y)

#Get values To Points
for row in toCursor:
    X = row.getValue("POINT_X")
    Y = row.getValue("POINT_Y")
    toPntX.append(X)
    toPntY.append(Y)

#Counter used for iteration through point lists
cntr=0

#List setup for calculating distances
distanceList = []
minList = []
indexList =[]
b = distanceList

#Ranges for From/To Points for iterations
fromRange = len(fromPntX)
toRange = len(toPntX)

#While Loop for item in From Points
while(cntr<fromRange):
    X1 = fromPntX[cntr]
    Y1 = fromPntY[cntr]
    cntr2=0
    #While Loop of item in To Points while referencing iteration of from point
    while(cntr2<toRange):
        X2 = toPntX[cntr2]
        Y2 = toPntY[cntr2]
        a = math.fabs(X1-X2)
        b = math.fabs(Y1-Y2)
        c = (a*a) + (b*b)
        h = math.sqrt(c)
        distanceList.append(h)
        cntr2+=1
    #Increase Counter
    cntr+=1
    #Calculate values and append to list
    value = min(distanceList)
    index = distanceList.index(value)
    indexList.append(index)
    minList.append(value)
    del distanceList[:]
    del cntr2
x=0

#Use Insert Cursor to update standalone table
for s in range(0, fromRange):
    irow = tableCursor.newRow()
    irow.setValue("Start_X", fromPntX[x])
    irow.setValue("Start_Y", fromPntY[x])
    irow.setValue("End_X", toPntX[indexList[x]])
    irow.setValue("End_Y", toPntY[indexList[x]])
    tableCursor.insertRow(irow)
    x +=1
del irow
del tableCursor
del cntr
del toPntX
del toPntY
del fromPntX
del fromPntY

#Create a shapefile from the standalone table that draws lines between two features
arcpy.XYToLine_management(table, os.path.join(output, "Near_Lines"), "Start_X", "Start_Y", "End_X", "End_Y", "", "", coordSystem)