import arcpy, os

#Please change to reflect your environment
gdb = r'Database Connections\c1022.sde'

for dir, dpath, files in arcpy.da.Walk(gdb):
    for f in files:
        path = os.path.join(dir,f)
        desc = arcpy.Describe(path)
        if desc.editorTrackingEnabled:
            errCNT = 0
            print '\n{0}/{1}'.format(os.path.basename(dir), f)
            if not desc.creatorFieldName == 'created_user':
                print '\t{0:20} {1}'.format('Creator Field:', desc.creatorFieldName)
                errCNT += 1
            if not desc.createdAtFieldName == 'created_date':
                print '\t{0:20} {1}'.format('Created Date:', desc.createdAtFieldName)
                errCNT += 1
            if not desc.editorFieldName == 'last_edited_user':
                print '\t{0:20} {1}'.format('Last Mod. Field:', desc.editorFieldName)
                errCNT += 1
            if not desc.editedAtFieldName == 'last_edited_date':
                print '\t{0:20} {1}'.format('Last Mod. Date:', desc.editedAtFieldName)
                errCNT += 1
            if desc.isTimeInUTC:
                print '\t{0:20} {1}'.format('Time Storage:', 'UTC')
                errCNT += 1
            if errCNT == 0:
                print '\tNo errors encountered'
            if not errCNT == 0:
                print '\t{} error(s) encountered'.format(errCNT)


##        if not desc.editorTrackingEnabled:
##            print 'Attempting to enable editor tracking on: {0}/{1}'.format(os.path.basename(dir), f)
##            try:
##                arcpy.EnableEditorTracking_management(path, 'created_user', 'created_date', 'last_edited_user', 'last_edited_date',  'ADD_FIELDS', 'DATABASE_TIME')
##                print '\tEnabled'
##            except:
##                print '\tFailed to Enable'
