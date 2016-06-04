import arcpy, os, subprocess, time

outPath = os.path.join(os.path.expanduser('~'), 'DelVersions.bat')

gdb = r"Database Connections\Connection to supt000073.sde"

cmd = "\nsdeversion -o delete -V {0} -i sde:oracle11g:supt000049/gmp -u sde -p sde -N -q"

outFile = open(outPath, 'w')

cnt = 0
for ver in arcpy.da.ListVersions(gdb):
    if '.WR' in ver.name.upper():
        outFile.write(cmd.format(ver.name))

outFile.close()
print "File located here: {}".format(outPath)