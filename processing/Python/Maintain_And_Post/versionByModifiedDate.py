import arcpy, datetime
gdb = r"Database Connections\Connection to supt02925.sde"
cnt = 0
for ver in arcpy.da.ListVersions(gdb):
    if ver.lastModified >= datetime.datetime.now() - datetime.timedelta(days=30):
        print ver.name, ver.lastModified
        cnt += 1
print cnt