import arcpy, os, sys, traceback

gdb = r'C:\Users\chri6962\AppData\Roaming\ESRI\Desktop10.3\ArcCatalog\Connection to cwells.sde'

versions = arcpy.da.ListVersions(gdb)

for version in versions:
    if version.name != 'SDE.DEFAULT':
        print 'Reconciling version: {0}'.format(version.name)
        try:
            arcpy.ReconcileVersions_management(gdb,
                                                'ALL_VERSIONS',
                                                'sde.DEFAULT',
                                                version.name,
                                                'LOCK_ACQUIRED',
                                                'ABORT_CONFLICTS',
                                                'BY_OBJECT',
                                                'FAVOR_TARGET_VERSION',
                                                'POST',
                                                'KEEP_VERSION')
            print arcpy.GetMessages(1)

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                              limit=2, file=sys.stdout)