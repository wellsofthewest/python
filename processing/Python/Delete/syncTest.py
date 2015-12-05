import arcpy
arcpy.SynchronizeChanges_management(geodatabase_1="//cwells/share/arcgis on julia.esri.com (user)/cwells1022.GeoDataServer",
                                    in_replica="SDE.cwells_sync_test",
                                    geodatabase_2="//cwells/share/Connection to JULIA.sde",
                                    in_direction="FROM_GEODATABASE1_TO_2",
                                    conflict_policy="IN_FAVOR_OF_GDB1",
                                    conflict_definition="BY_OBJECT",
                                    reconcile="DO_NOT_RECONCILE")