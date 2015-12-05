import arcpy
import codecs
import sys
import os

fc = r'C:\Work\TechAssist\Liting\Connection to benlin (3).sde\parent.SDE.DMS_TEST'
fields = ['OBJECTID','DMS_VALUE']

textfile = os.path.join("C:\\Work\\TechAssist\\Liting\\", "DMS_String.csv")

textfile = codecs.open(textfile, "wb", "utf-8")

with arcpy.da.SearchCursor(fc, fields) as cursor:
        for row in cursor:
                strout = str(row[0]) + ' | ' + row[1]
                textfile.write(strout + '\r\n')
            
textfile.close()

print 'Done.'
