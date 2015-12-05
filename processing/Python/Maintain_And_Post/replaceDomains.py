import arcpy, os

gdb = <Path to feature dataset>

for dir, dirpath, files in arcpy.da.Walk(gdb):
    for file in files:
        fc = os.path.join(dir, file)
        fldlist = arcpy.ListFields(fc)
        print fc
        for fld in fldlist:
            if fld.domain[-2:] == '_1':
                print "\t{} found on {}".format(fld.domain, fld.name)
                #arcpy.AssignDomainToField_management(fc, fld.name, fld.domain[:-2])


