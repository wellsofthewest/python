import struct, arcpy, os

arcpy.env.overwriteOutput = True

path = os.path.expanduser('~')

gdb_name = 'WKB_Sample.gdb'
fc_name = 'WKB_Polygon'

if os.path.exists(os.path.join(path,gdb_name)):
    pass
else:
    arcpy.CreateFileGDB_management(path, gdb_name)

if arcpy.Exists(os.path.join(path,gdb_name,fc_name)):
    pass
else:
    arcpy.CreateFeatureclass_management(os.path.join(path, gdb_name), fc_name, 'POLYGON', spatial_reference=4326)

wkbarray = bytearray()

#WKB ENDIAN
endian = struct.pack('b', 1)

#WKB TYPE
wkbtype = struct.pack('i', 3)

#RINGS
rings = struct.pack('i', 1)

#POINTS
numpoints = struct.pack('i', 4)

wkbarray.extend(endian)
wkbarray.extend(wkbtype)
wkbarray.extend(rings)
wkbarray.extend(numpoints)


wkbarray.extend(struct.pack('d', 0))
wkbarray.extend(struct.pack('d', 0))
wkbarray.extend(struct.pack('d', 50))
wkbarray.extend(struct.pack('d', 50))
wkbarray.extend(struct.pack('d', 50))
wkbarray.extend(struct.pack('d', 0))
wkbarray.extend(struct.pack('d', 0))
wkbarray.extend(struct.pack('d', 0))

fc = os.path.join(path,gdb_name,fc_name)
cur = arcpy.da.InsertCursor(fc, ['SHAPE@WKB'])
cur.insertRow([wkbarray])
del cur




