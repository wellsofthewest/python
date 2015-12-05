import arcpy, os
from arcpy import env

# set system environments
env.workspace = r'D:\Resources\Programming\Python\Exercises\Subtypes.gdb'
arcpy.env.overwriteOutput = True


# find the list of datasets
datasetList = arcpy.ListDatasets("*", "Feature")
for dataset in datasetList:
    fcList = arcpy.ListFeatureClasses("*", "", dataset)
    # find the list of feature classes in the dataset
    for fc in fcList:
                rows = arcpy.SearchCursor(table)
                # set the counter for the subtype code
                # for each table, get the default value that corresponds with the subtype description
                for row in rows:
                    defaultvalue = row.getValue("CODE")
                    description = row.getValue("FULLNAME")
                    subtype = str(x) + ": " + description
                    # add the value to the feature classes
                    arcpy.AssignDefaultToField_management(fc, "FIELDCODE", defaultvalue, subtype )

