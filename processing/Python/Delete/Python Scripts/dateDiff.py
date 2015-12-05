import arcpy
import time
import datetime

fc = "c:/Data/time.gdb/gravityMain"
fields = ('LASTUPDATE','STATUS')
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

# Create update cursor for feature class 
with arcpy.da.UpdateCursor(fc, fields) as cursor:
    # For each row, evaluate the WELL_YIELD value (index position 
    #  of 0), and update WELL_CLASS (index position of 1)
    for row in cursor:
        insp_date = str(row[0])[:18]
        timeCast = time.mktime(datetime.datetime.strptime(insp_date, '%Y-%m-%d %H:%M:%S').timetuple())
        if ts - timeCast > 3.154e+7:
            row[1] = "Expired"

print "Done"