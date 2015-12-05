import arcpy, os

for dir, dirnames, files in arcpy.da.Walk(r'C:\arcgis\ArcTutor\BuildingaGeodatabase\Montgomery.gdb'):
    for f in files:
        path = os.path.join(dir, f)
        flds = arcpy.ListFields(path)
        print 'Feature Class:', f
        for fld in flds:
            if fld.domain == 'Material':
                print '\tField:', fld.name
        try:
            subtypes = arcpy.da.ListSubtypes(path)
            for stcode, stdict in subtypes.iteritems():
                for stkey in stdict.iterkeys():
                    if stkey == 'FieldValues':
                        fields = stdict[stkey]
                        for field, fieldvals in fields.iteritems():
                            if not fieldvals[1] is None:
                                if fieldvals[1].name == 'Material':
                                    print '\tSubtype [Field]: {0} [{1}]'.format(stdict['Name'], field)
        except:
            print 'Cannot gather subtypes for:', f