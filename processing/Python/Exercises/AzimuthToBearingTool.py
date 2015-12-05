#Azimuth to Bearing Script Tool
#
#Author: Christian Wells
#Publication Date: 07/31/2012
#Copyright: Esri
#
#
#Use:
#The production and support of python scripts is
#beyond the scope of support for Esri.
#Although I have provided you with a possible
#python solution to a problem, this script its
#future customizations and/or uses must be managed
#and/or modified by the user and/or their staff

import arcpy, os
arcpy.env.overwriteOutput = True

#Set Parameters for Script Tool Inputs

#Select Feature Layer
fc = arcpy.GetParameterAsText(0)

#Select Azimuth Field within selected Feature Layer
field = arcpy.GetParameterAsText(1)

#Select the Field which the bearing will be stored in
bearingField = arcpy.GetParameterAsText(2)

#Create Lists to store the derived prefix, suffix, and bearing
prefix = []
suffix = []
bearing = []
prefixSet = ()
suffixSet = ()
bearingSet = ()

#Create a counter for list iteration
p = 0
s = 0
b = 0

#Use Update Cursor to derive the correct direction and bearing from Azimuth
rows = arcpy.UpdateCursor(fc, "", "", "", "")
for row in rows:
    value = row.getValue(field)       
    if value >= 0 and value < 90:
        Prefix = "N"
        Suffix = "E"
        Bearing = value
        if Prefix not in prefixSet:
            prefix.append(Prefix)
        if Suffix not in suffixSet:
            suffix.append(Suffix)
        if Bearing not in bearingSet:
            bearing.append(Bearing)
    elif value >= 90 and value < 180:
        Prefix = "S"
        Suffix = "E"
        Bearing = value
        if Prefix not in prefixSet:
            prefix.append(Prefix)
        if Suffix not in suffixSet:
            suffix.append(Suffix)
        if Bearing not in bearingSet:
            bearing.append(180 - Bearing)
    elif value >= 180 and value < 270:
        Prefix = "S"
        Suffix = "W"
        Bearing = value
        if Prefix not in prefixSet:
            prefix.append(Prefix)
        if Suffix not in suffixSet:
            suffix.append(Suffix)
        if Bearing not in bearingSet:
            bearing.append(270 - Bearing)
    elif value >= 270 and value < 360:
        Prefix = "N"
        Suffix = "W"
        Bearing = value
        if Prefix not in prefixSet:
            prefix.append(Prefix)
        if Suffix not in suffixSet:
            suffix.append(Suffix)
        if Bearing not in bearingSet:
            bearing.append(360 - Bearing)
    #Update the Bearing Field with the new bearing values from the lists
    Bearing = str(bearingField)
    row.Bearing = prefix[p] + str(bearing[b]) + suffix[s]
    rows.updateRow(row)
    p = p + 1
    s = s + 1
    b = b + 1
del row
del rows


  

