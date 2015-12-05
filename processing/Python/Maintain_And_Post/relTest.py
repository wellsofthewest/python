import arcpy, os, sys

gdb =sys.argv[1]


print '\nPlease enter the users that will have EDIT privileges on the intermediate table, separated by commas. \nIf none, please press enter.'
eImp = raw_input('\nEdit Users: ')

print '\nPlease enter the users that will have VIEW privileges on the intermediate table, separated by commas. \nIf none, please press enter.'
vImp = raw_input('\nView Users: ')

editUsers = []
viewUsers = []

editors = eImp.replace(' ','')
viewers = vImp.replace(' ','')

if len(editors) > 0:
    for user in editors.split(','):
        editUsers.append(user)
if len(viewers) > 0:
    for user in viewers.split(','):
        viewUsers.append(user)

walk = arcpy.da.Walk(gdb, datatype=['RelationshipClass'])


for dir, path, file in walk:
    for f in file:
        relClass = os.path.join(dir, f)
        desc = arcpy.Describe(relClass)
        if desc.isAttributed == True or desc.cardinality == 'ManyToMany':
            print f
            if len(editUsers) > 0:
                print '\tGrant EDIT privileges to:'
                for eUser in editUsers:
                    print '\t\t{}'.format(eUser)
                    arcpy.ChangePrivileges_management(relClass, eUser, 'GRANT', 'GRANT')
            if len(viewUsers) > 0:
                print '\tGrant VIEW privileges to:'
                for vUser in viewUsers:
                    print '\t\t{}'.format(vUser)
                    arcpy.ChangePrivileges_management(relClass, vUser, 'GRANT', 'AS_IS')
