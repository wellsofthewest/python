'''
This script, when run, will change values of records.  Please ensure
this script is tested before running against production data.  Custom
scripts is beyond the scope ofEsri Support Services. No warranties 
or guarantees of any kind can be made.

For more information regarding the functions used in this script, 
please see the following links:

Python Time module:
http://docs.python.org/2/library/time.html

Python datetime:
http://docs.python.org/2/library/datetime.html?highlight=datetime#datetime

Arcpy Data Access Module:
http://resources.arcgis.com/en/help/main/10.1/index.html#/What_is_the_data_access_module/018w00000008000000/
'''

import arcpy
import time
import datetime

# Geodatabase connection file/Feature Dataset/Feature Class
fc = r"C:\Users\ken6574\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\BEHAVIOR@SDE.sde\Backflow\Backflow"
# Columns to process:
fields = ('INSP_DATE','STATUS')
#Current time as unix timestamp.
ts = time.time()

# Create update cursor for feature class 
with arcpy.da.UpdateCursor(fc, fields) as cursor:
    # For each row, evaluate the INSP_DATE value (index position 
    #  of 0), and update STATUS (index position of 1)
    for row in cursor:
        # Check for null values in the insp_date field.
        if row[0] is not None:
            # Cast date data to a string.
            insp_date = str(row[0])[:10]
            # Re-cast the new date string to a unix_timestamp
            timeCast = time.mktime(datetime.datetime.strptime(insp_date, '%Y-%m-%d').timetuple())
            # Check the insp_date timestamp is greater than or equal
            # to the amount of seconds in a year.
            if ts - timeCast >= 3.154e+7:
                # Set the STATUS column to Expired if criteria is met.
                row[1] = "Expired"
                # Present processing of each row.
                print insp_date + " has expired.  STATUS has been updated"

print "Done"