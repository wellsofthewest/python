import arcpy, sys, os

arcpy.env.overwriteOutput = True

root = 'c:/demos'
folder = os.path.join(root, 'PyGDB')
sdeConn = 'sde@c1022.sde'
saConn = 'sa@c1022.sde'

dsDict = {'Water':2272, 'Zoning':2272, 'Political':2272}

fcDict = {'Mains':{'dataset':'Water','geometry_type':'POLYLINE', 'has_m':'ENABLED', 'has_z':'ENABLED', 'config_keyword':'GEOMETRY'},
        'Laterals':{'dataset':'Water','geometry_type':'POLYLINE', 'has_m':'ENABLED', 'has_z':'ENABLED', 'config_keyword':'GEOMETRY'},
        'Valves':{'dataset':'Water','geometry_type':'POINT', 'has_m':'DISABLED', 'has_z':'ENABLED', 'config_keyword':'GEOMETRY'},
        'Hydrants':{'dataset':'Water','geometry_type':'POINT', 'has_m':'DISABLED', 'has_z':'ENABLED', 'config_keyword':'GEOMETRY'},
        'Parcels':{'dataset':'Zoning','geometry_type':'POLYGON', 'has_m':'DISABLED', 'has_z':'DISABLED', 'config_keyword':'GEOMETRY'},
        'Buildings':{'dataset':'Zoning','geometry_type':'POLYGON', 'has_m':'DISABLED', 'has_z':'DISABLED', 'config_keyword':'GEOMETRY'},
        'Street_Centerlines':{'dataset':'Zoning','geometry_type':'POLYLINE', 'has_m':'ENABLED', 'has_z':'ENABLED', 'config_keyword':'GEOMETRY'},
        'Parks':{'dataset':'Zoning','geometry_type':'POLYGON', 'has_m':'DISABLED', 'has_z':'DISABLED', 'config_keyword':'GEOMETRY'},
        'Boundary':{'dataset':'Political','geometry_type':'POLYGON', 'has_m':'DISABLED', 'has_z':'DISABLED', 'config_keyword':'GEOMETRY'},
        'Districts':{'dataset':'Political','geometry_type':'POLYGON', 'has_m':'DISABLED', 'has_z':'DISABLED', 'config_keyword':'GEOMETRY'},
        'Wards':{'dataset':'Political','geometry_type':'POLYGON', 'has_m':'DISABLED', 'has_z':'DISABLED', 'config_keyword':'GEOMETRY'},
        'Streets':{'dataset':'Political','geometry_type':'POLYGON', 'has_m':'DISABLED', 'has_z':'DISABLED', 'config_keyword':'GEOMETRY'}}

usDict = {'WaterEdit':{'in_dataset':'Water', 'View':'GRANT', 'Edit':'GRANT'},
        'WaterRead':{'in_dataset':'Water', 'View':'GRANT', 'Edit':'AS_IS'},
        'ZoneEdit':{'in_dataset':'Zoning', 'View':'GRANT', 'Edit':'GRANT'},
        'ZoneRead':{'in_dataset':'Zoning', 'View':'GRANT', 'Edit':'AS_IS'},
        'MasterEdit':{'in_dataset':['Zoning', 'Water', 'Political'], 'View':'GRANT', 'Edit':'GRANT'}}

hydrants = [(2371914.05957,262238.479384),
(2372455.72614,262894.729384),
(2372539.05963,262327.020873),
(2372346.35103,261811.39592),
(2372445.30949,261129.104306),
(2372195.30966,260509.312567),
(2372846.35134,260597.854384),
(2373023.43465,261212.437801),
(2373143.22607,262332.229196),
(2373033.85129,262978.06255),
(2371997.39274,263540.562738),
(2372507.80937,264399.937659),
(2371622.39283,261014.520874),
(2371674.47606,260722.854462),
(2372096.3512,259806.187661),
(2372544.26795,260170.770921),
(2373190.10131,260264.521061),
(2372419.26788,260847.854212),
(2372096.3512,261097.854369),
(2372028.643,261587.437707),
(2371976.55944,261920.77103)]

if os.path.exists(folder) == False:
    os.mkdir(folder)

if os.path.exists(os.path.join(folder, sdeConn)) == False:
    arcpy.CreateDatabaseConnection_management(folder, 'sde@c1022.sde', 'SQL_SERVER', 'cwells', 'DATABASE_AUTH', 'SDE', 'sde', database='c1022')
if os.path.exists(os.path.join(folder, saConn)) == False:
    arcpy.CreateDatabaseConnection_management(folder, 'sa@c1022.sde', 'SQL_SERVER', 'cwells', 'DATABASE_AUTH', 'sa', 'sa', database='c1022')

gdb = os.path.join(folder, sdeConn)

arcpy.env.workspace = gdb

for ds, sr in dsDict.iteritems():
    arcpy.CreateFeatureDataset_management(os.path.join(folder, sdeConn), ds, sr)

for fc, fcDef in fcDict.iteritems():
    arcpy.CreateFeatureclass_management(fcDef['dataset'],
                                        fc,
                                        geometry_type=fcDef['geometry_type'],
                                        has_m=fcDef['has_m'],
                                        has_z=fcDef['has_z'],
                                        config_keyword=fcDef['config_keyword'])

for ds, sr in dsDict.iteritems():
    arcpy.RegisterAsVersioned_management(ds)


for user, userDef in usDict.iteritems():
    arcpy.CreateDatabaseUser_management(os.path.join(folder, saConn),
                                        user_authentication_type="DATABASE_USER",
                                        user_name=user,
                                        user_password="sde")

    arcpy.ChangePrivileges_management(in_dataset=userDef['in_dataset'],
                                      user=user,
                                      View=userDef['View'],
                                      Edit=userDef['Edit'])

    if os.path.exists(os.path.join(folder, '{0}@c1022.sde'.format(user))) == False and userDef['Edit'] == 'GRANT' and user == 'MasterEdit':
        arcpy.CreateDatabaseConnection_management(folder, '{0}@c1022.sde'.format(user), 'SQL_SERVER', 'CWELLS', 'DATABASE_AUTH', user, 'sde', database='c1022')

    if os.path.exists(os.path.join(folder, '{0}@c1022.sde'.format(user))) == False and userDef['Edit'] == 'AS_IS':
        arcpy.CreateDatabaseConnection_management(folder, '{0}@c1022.sde'.format(user), 'SQL_SERVER', 'CWELLS', 'DATABASE_AUTH', user, 'sde', database='c1022')


arcpy.CreateVersion_management(os.path.join(folder, 'MasterEdit@c1022.sde'), 'sde.DEFAULT', 'MasterEdit')

for user, userDef in usDict.iteritems():
    if userDef['Edit'] == 'GRANT' and user != 'MasterEdit':
        arcpy.CreateVersion_management(os.path.join(folder, 'MasterEdit@c1022.sde'), 'MASTEREDIT.MasterEdit', user, 'PUBLIC')
        arcpy.CreateDatabaseConnection_management(folder, '{0}@c1022.sde'.format(user), 'SQL_SERVER', 'CWELLS', 'DATABASE_AUTH', user, 'sde', database='c1022', version_type='TRANSACTIONAL', version='MASTEREDIT.{0}'.format(user))


edit = arcpy.da.Editor(os.path.join(folder, 'WaterEdit@c1022.sde'))

edit.startEditing(False, True)

edit.startOperation()

with arcpy.da.InsertCursor(os.path.join(folder, 'WaterEdit@c1022.sde', 'c1022.sde.Water', 'c1022.sde.Hydrants'), ('SHAPE@')) as icur:
    for row in hydrants:
        icur.insertRow([row])

edit.stopOperation()

edit.stopEditing(True)


arcpy.ReconcileVersions_management(os.path.join(folder, 'MasterEdit@c1022.sde'),
                                    'ALL_VERSIONS',
                                    'MASTEREDIT.MasterEdit',
                                    ['MASTEREDIT.WaterEdit', 'MASTEREDIT.ZoneEdit'],
                                    'NO_LOCK_ACQUIRED',
                                    'NO_ABORT',
                                    'BY_OBJECT',
                                    'FAVOR_TARGET_VERSION',
                                    'POST',
                                    'DELETE_VERSION')

arcpy.ReconcileVersions_management(gdb,
                                    'ALL_VERSIONS',
                                    'sde.DEFAULT',
                                    'MASTEREDIT.MasterEdit',
                                    'NO_LOCK_ACQUIRED',
                                    'NO_ABORT',
                                    'BY_OBJECT',
                                    'FAVOR_TARGET_VERSION',
                                    'POST',
                                    'DELETE_VERSION')
##
##
##
##
##
##
##
##
##

