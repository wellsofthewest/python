import arcpy, os

verName = 'testing3'
verParent = 'sde.default'
gdb = r'Database Connections\Connection to cwells.sde'

desc = arcpy.Describe(gdb)
cp = desc.connectionProperties

verList = [v.upper() for v in arcpy.ListVersions(gdb)]

cVersion = '{}.{}'.format(cp.user, verName)

if cVersion.upper() not in verList:
    print '{} does not exist. Creating...'.format(cVersion.upper())
    arcpy.CreateVersion_management(gdb, verParent, verName)
    print 'Version created. Exiting.'
else:
    print '{} exists. Exiting.'.format(cVersion.upper())