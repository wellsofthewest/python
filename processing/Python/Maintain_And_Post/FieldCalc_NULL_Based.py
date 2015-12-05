import arcpy

workspace = r"Database Connections\Connection to CWELLS (5).sde"
arcpy.env.workspace=workspace
fcList = arcpy.ListFeatureClasses()
for fc in fcList:
    print fc
    fields = arcpy.ListFields(fc, "", "String")
    for field in fields:
        print field.name
        exp = """if IsNull([{0}]) then
            f2 = " "
            else
            f2 = [{0}]
            end if""".format(field.name)

        arcpy.CalculateField_management(fc,field.name,"f2","VB",exp)
