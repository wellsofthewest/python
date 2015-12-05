import os, sys
import arcpy
arcpy.env.overwriteOutput = True

arcpy.env.workspace = r"M:\dep\Master_Geodatabases\Hardbacks\Master_DEP_Template.gdb"
gdb = r"M:\dep\Master_Geodatabases\Hardbacks\Master_DEP_Template.gdb"
gdb2 =r"M:\gis\Geodatabases\_MOA_Quad_Template.gdb"

desc = arcpy.Describe(gdb)
domains = desc.Domains
print domains

for domain in domains:
    print '\nExporting %s CV to table in %s' % (domain, gdb)
    table = os.path.join(gdb, domain)
    arcpy.DomainToTable_management(gdb, domain, table, 'field','Description', '#')

tblList = arcpy.ListTables()
for table in tblList:
    tbl = table
    print '\tImporting %s Table to Domain in %s' % (table, gdb)
    arcpy.TableToDomain_management(table, 'field', 'Description', gdb2, tbl)
    print '\tDeleting %s Table from %s\n' % (tbl, gdb)
    arcpy.Delete_management(table)

