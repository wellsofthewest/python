import arcpy
import os
arcpy.env.overwriteOutput = True
tempWorkpath = r"C:\Users\chri0000\Desktop\Internship\WaterProject\Temp.gdb"
precipWorkpath = r"C:\Users\chri0000\Desktop\Internship\WaterProject\Precip.gdb"

arcpy.env.workspace = r"C:\Users\chri0000\Desktop\Internship\WaterProject\Temp.gdb"

da = 1951
db = 1952

for ras in arcpy.ListDatasets():
    while (db < 2012):
        c = "Temp_"
        d = c + str(da)
        e = c + str(db)
        subtract = arcpy.sa.Minus(e, d)
        divide = arcpy.sa.Divide(subtract, d)
        print 'Saving Percent Change from %s to %s' % (da, db)
        divide.save(tempWorkpath + os.sep + "PctChg_" + str(da) + "_" + str(db))
        da += 1
        db += 1

arcpy.env.workspace = r"C:\Users\chri0000\Desktop\Internship\WaterProject\Precip.gdb"

da = 1951
db = 1952

for ras in arcpy.ListDatasets():
    while (db < 2012):
        c = "Precip_"
        d = c + str(da)
        e = c + str(db)
        subtract = arcpy.sa.Minus(e, d)
        divide = arcpy.sa.Divide(subtract, d)
        print 'Saving Percent Change from %s to %s' % (da, db)
        divide.save(tempWorkpath + os.sep + "PctChg_" + str(da) + "_" + str(db))
        da += 1
        db += 1
