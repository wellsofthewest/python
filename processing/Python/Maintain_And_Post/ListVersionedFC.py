import arcpy, os

#Please change to reflect your environment
gdb = r'Database Connections\c1022.sde'

for dir, dpath, files in arcpy.da.Walk(gdb):
    for f in files:
        path = os.path.join(dir,f)
        desc = arcpy.Describe(path)
        print '\n{0}/{1}'.format(os.path.basename(dir), f)
        print '\tVersioned: {}'.format(desc.isVersioned)