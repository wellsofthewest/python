import arcpy, os, sys, time

gdb = r'Database Connections\Connection to cwells.sde'

editUsers = ['editor']
viewUsers = ['viewer']

walk = arcpy.da.Walk(gdb, datatype=['RelationshipClass'])


for dir, path, file in walk:
    for f in file:
        relClass = os.path.join(dir, f)
        desc = arcpy.Describe(relClass)
        if desc.isAttributed == True or desc.cardinality == 'ManyToMany':
            print '\n',f
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

time.sleep(5)
