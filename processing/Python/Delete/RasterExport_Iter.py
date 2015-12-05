import arcpy
import os
arcpy.env.overwriteOutput = True

workpath = r"C:\Users\chri0000\Desktop\Internship\WaterProject\CaliforniaWaterProject.gdb"
fc = r"C:\Users\chri0000\Desktop\Internship\WaterProject\CaliforniaWaterProject.gdb\QueryTable_project"
ordKrig = arcpy.sa.KrigingModelOrdinary("EXPONENTIAL", "", "", "", "")
temp = "Air_Max_Avg_"
precip = "Ann_Precip_"

tempWorkpath = r"C:\Users\chri0000\Desktop\Internship\WaterProject\Temp.gdb"
precipWorkpath = r"C:\Users\chri0000\Desktop\Internship\WaterProject\Precip.gdb"

for year in range(1951, 2012):
    arcpy.MakeFeatureLayer_management(fc, "layer", "\"ClimateDataByStation_Date_\" = %s" % year)
    print 'Performing Kriging Precipitation Interpolation for %s' % year
    outKrig = arcpy.sa.Kriging("layer", "ClimateDataByStation_Precip", ordKrig)
    print '  Copying Kriging Precipitation Interpolation for %s' % year
    arcpy.CopyRaster_management(outKrig, os.path.join(precipWorkpath, "Precip_" + str(year)))
    print '  Performing Kriging Max Temp Interpolation for %s' % year
    outKrig = arcpy.sa.Kriging("layer", "ClimateDataByStation_Air_max", ordKrig, "", "", "")
    print '  Copying Kriging Max Temp Interpolation for %s\n' % year
    arcpy.CopyRaster_management(outKrig, os.path.join(tempWorkpath, "Temp_" + str(year)))
