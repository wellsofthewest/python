#Christian Wells
#IMAPS 2013
#
#Name: Find field entries using cursors
#
#Purpose: This tool uses the arcpy and os module to determine the information in a
#specific field. The tool is very diverse and often used with different variables or
#SQL statements to find row information. This was used for the QA/QC process during
#export of RP data for DEP

import arcpy
import os

Elevations = r"M:\dep\Master_Geodatabases\Hardbacks\Master_DEP_Template.gdb\Master_Coal_Seam_Elevations_Template"
MOA = r"M:\dep\Master_Geodatabases\Hardbacks\Master_DEP_Template.gdb\Master_Digitized_Mined_Area_Template"
Index = r"M:\dep\Master_Geodatabases\Hardbacks\Master_DEP_Template.gdb\Master_IUP_Mine_Map_Index_Template"

MissingMOA = []
MissEle= []

'''
Process Explanation
1 - Completed
2 - Needs QC
3 - In Progress
4 - Not Completed
5 - No Data

'''

rowsMOA = arcpy.SearchCursor(MOA, "", "", "", "")
rowsIndex = arcpy.SearchCursor(Index, "\"MinedAreaDigitization\" = '1'", "", "", "ID_Sort A")
rowElevations = arcpy.SearchCursor(Elevations, "", "", "", "")
web = r"M:\dep\GIS_Project\Digitization"

for row in rowsMOA:
    value = row.getValue("Source")
    value2 = value[19:]
    if value2 not in MissingMOA:
        MissingMOA.append(value2)

for row in rowsIndex:
    value = row.getValue("ID_Sort")
    if value not in MissingMOA:
        print value

