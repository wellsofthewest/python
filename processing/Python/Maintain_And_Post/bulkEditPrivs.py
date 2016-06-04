import arcpy

gdb = r"Database Connections\Connection to strahan.sde"

conn = arcpy.ArcSDESQLExecute(gdb)

tblList = conn.execute("SELECT table_name FROM information_schema.tables where TABLE_CATALOG = 'mainEdit' and TABLE_SCHEMA = 'sifu'")

for table in tblList:
    conn.execute('grant select, insert, update, delete on {} to "AVWORLD\jays7539"'.format(table[0]))