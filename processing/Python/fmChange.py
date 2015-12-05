import arcpy, os

# Place the path to the data here
fc = r"C:\ConnFile.sde\FeatureClass"

## These are the fields to keep
fieldsToKeep = ["STATION", "STATE", "LATITUDE", "LONGITUDE"]

## Create a blank field mapping
fms = arcpy.FieldMappings()

## Create a dictionary with current names (keys) set to new names (values)
fldsNamesDict = {"STATION":"STN","STATE":"ST","LATITUDE":"LAT","LONGITUDE":"LON"}

## Loop through all the field in the feature class
for field in arcpy.ListFields(fc):

    ## If the name in the feature class is in fieldsToKeep, continue;
    if field.name in fldList:

        ## Create an empty field map which will be generated for each new iteration
        fm = arcpy.FieldMap()

        ## Add the current field to the field map
        fm.addInputField(fc, field.name)

        ## Set the name in the field map to the new name from the dictionary (fldsNamesDict)
        fm_name = fm.outputField
        fm_name.name = fldsNamesDict[field.name]
        fm.outputField = fm_name

        ## Add the field map to the field mappings
        fms.addFieldMap(fm)

## Export the feature class to a shapefile with the above field mappings
arcpy.FeatureClassToFeatureClass_conversion(in_Features = fc,
                                            out_path = "Path\to\folder", # Please set a folder variable here to the output destination
                                            out_name = "shapefile Name", # Please set a output name here
                                            field_mapping = fms)


