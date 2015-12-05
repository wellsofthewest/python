import arcpy, os, struct

gdb = os.path.join(os.getcwd(), 'WKB.gdb')
fc = 'LINESTRING'

arcpy.env.workspace = gdb

rows = arcpy.da.SearchCursor(fc, ['SHAPE@', 'SHAPE@WKB'])

for row in rows:
    print("Geometry WKB Property Byte: {}".format(len(row[0].WKB)))
    print "\tType: {}".format(struct.unpack('i',row[0].WKB[1:5])[0])
    print "\tNumRings: {}".format(struct.unpack('i',row[0].WKB[5:9])[0])
    print "\tNumPoints: {}".format(struct.unpack('i',row[0].WKB[9:13])[0])
    print "\tPoint 1 (X): {}".format(struct.unpack('d',row[0].WKB[9:17])[0])
    print "\tPoint 1 (Y): {}".format(struct.unpack('d',row[0].WKB[17:25])[0])
    print "\tPoint 2 (X): {}".format(struct.unpack('d',row[0].WKB[25:33])[0])
    print "\tPoint 2 (Y): {}".format(struct.unpack('d',row[0].WKB[33:41])[0])
    print("\nCursor WKB Token Byte: {}".format(len(row[1])))
    print "\tType: {}".format(struct.unpack('i',row[1][1:5])[0])
    print "\tNumPoints: {}".format(struct.unpack('i',row[1][5:9])[0])
    print "\tPoint 1 (X): {}".format(struct.unpack('d',row[1][9:17])[0])
    print "\tPoint 1 (Y): {}".format(struct.unpack('d',row[1][17:25])[0])
    print "\tPoint 2 (X): {}".format(struct.unpack('d',row[1][25:33])[0])
    print "\tPoint 2 (Y): {}".format(struct.unpack('d',row[1][33:41])[0])
