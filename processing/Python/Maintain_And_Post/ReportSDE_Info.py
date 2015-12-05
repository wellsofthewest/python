import arcpy, os

gdb = r"C:\demos\PyGDB\sde@c1022.sde"

arcpy.env.workspace = gdb

dsList = arcpy.ListDatasets()
dsList.sort()
for ds in dsList:
    print "{0}{1}".format("Dataset: ", ds)
    walk = arcpy.da.Walk(os.path.join(gdb,ds), topdown=True, datatype='FeatureClass')
    for dirpath, dirnames, filenames in walk:
        for fc in filenames:
            print "\t{0}{1}".format("Feature Class: ", fc)
            fieldList = arcpy.ListFields(dataset=os.path.join(gdb, ds, fc))
            for field in fieldList:
                print "\t\t{0:40}{1:40}".format(field.name, field.domain)
    walk = arcpy.da.Walk(os.path.join(gdb,ds), topdown=True, datatype='RelationshipClass')
    for dirpath, dirnames, filenames in walk:
        for fc in filenames:
            print "\t{0}{1}".format("Relationship Class: ", fc)
            desc = arcpy.Describe(fc)
            try:
                print "\t\t", desc.originClassNames
            except:
                print "No Origin FC"
            try:
                print "\t\t", desc.destinationClassNames
            except:
                print "No Destination FC"
walk = arcpy.da.Walk(gdb, topdown=True, datatype='FeatureClass')
for dirpath, dirnames, filenames in walk:
    for fc in filenames:
        print "\t{0}{1}".format("Feature Class: ", fc)
        fieldList = arcpy.ListFields(dataset=os.path.join(gdb, fc))
        for field in fieldList:
            print "\t\t{0:40}{1:40}".format(field.name, field.domain)

walk = arcpy.da.Walk((gdb), topdown=True, datatype='RelationshipClass')
for dirpath, dirnames, filenames in walk:
    for fc in filenames:
        print "\t{0}{1}".format("Relationship Class: ", fc)
        desc = arcpy.Describe(fc)
        print desc.originClassNames
        print desc.destinationClassNames

walk = arcpy.da.Walk(gdb, topdown=True, datatype='Table')
for dirpath, dirnames, filenames in walk:
    for fc in filenames:
        print "\t{0}{1}".format("Table: ", fc)
        fieldList = arcpy.ListFields(dataset=os.path.join(gdb, fc))
        for field in fieldList:
            print "\t\t{0:40}{1:40}".format(field.name, field.domain)


#Domains

domains = arcpy.da.ListDomains(gdb)
for domain in domains:
    print('\nDomain name: {0}'.format(domain.name))
    if domain.domainType == 'CodedValue':
        coded_values = domain.codedValues
        print('{0:40} {1}'.format("CODE:", "DESCRIPTION:"))
        for val, desc in coded_values.iteritems():
            print('{0:40} {1}'.format(val, desc))
    elif domain.domainType == 'Range':
        print('Min: {0}'.format(domain.range[0]))
        print('Max: {0}'.format(domain.range[1]))


