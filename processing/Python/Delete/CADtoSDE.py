# A batch import of CAD files into Geodatabase

#import system modules
import arcpy, os
from arcpy import env

#Set local variables
input_CAD_folder="C:\Users\qing7252\Desktop\Incidents\CAD_Disneyland\CAD\Disney_CAD"
output_gdb_folder="C:\Users\qing7252\Desktop\Incidents\CAD_Disneyland\CAD\Disney_CAD"
output_gdb="test.gdb"
output_gdb_path=os.path.join(output_gdb_folder, output_gdb)

reference_scale="1000"
spatial_reference="NAD_1983_StatePlane_California_VI_FIPS_0406_Feet"

#For loop iterate through every file in input folder

for found_file in os.listdir(input_CAD_folder):
    #Search  for .dwg files
    if found_file.endswith(".dwg"):
        
        print "Converting:"+found_file
        input_CAD_dataset=os.path.join(input_CAD_folder,found_file)
        try:
            arcpy.CADToGeodatabase_conversion(input_CAD_dataset,output_gdb_path, found_file[:-4], reference_scale, spatial_reference)
        except:
            print arcpy.GetMessage()




        
    
                


