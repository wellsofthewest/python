import arcpy, os, sys

gdb = r'C:\Users\chri6962\AppData\Roaming\ESRI\Desktop10.1\ArcCatalog\Connection to cwells.sde'

for dir, dirpath, files in arcpy.da.Walk(gdb, datatype=['RelationshipClass']):
    for file in files:
        path = os.path.join(dir, file)
        desc = arcpy.Describe(path)
                                print '\n', file
                                print("%-25s %s" % ("Backward Path Label:", desc.backwardPathLabel))
                                print("%-25s %s" % ("Cardinality:", desc.cardinality))
                                print("%-25s %s" % ("Class key:", desc.classKey))
                                print("%-25s %s" % ("Destination Class Names:", desc.destinationClassNames[0]))
                                print("%-25s %s" % ("Forward Path Label:", desc.forwardPathLabel))
                                print("%-25s %s" % ("Is Attributed:", desc.isAttributed))
                                print("%-25s %s" % ("Is Composite:", desc.isComposite))
                                print("%-25s %s" % ("Is Reflexive:", desc.isReflexive))
                                print("%-25s %s" % ("Key Type:", desc.keyType))
                                print("%-25s %s" % ("Notification Direction:", desc.notification))
                                print("%-25s %s" % ("Origin Class Names:", desc.originClassNames[0]))
                                print("%-25s %s" % ("Origin Primary Key:", desc.originClassKeys[0][0]))
                                print("%-25s %s" % ("Origin Foreign Key:", desc.originClassKeys[1][0]))
