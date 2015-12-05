import os

workPath = r"C:\Temp"

outLog = open(os.path.join(workPath, "LogFile10M.sql"), "w+")

minx = -178.2
miny = 18.9
maxx = -66.9
maxy = 71.4

cnt = 0

for i in range(10000001):
    miny += 0.0001
    if miny >= maxy:
        print "Next Row"
        miny = 18.9
        minx += 0.0001
        #print miny, minx
    outLog.write("insert into sde.streets_points values (sde.st_point({0},{1},4326));".format(minx, miny))
    cnt += 1
print cnt
print miny, minx

outLog.close()