'''
/***********************************************************************

build-wkb-polygon.py  --  Python creation of WKB polygon

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

Purpose:
 This script serves as a sample for creating a well-known binary (WKB)
polygon in Python and then inserting it in an ArcGIS file geodatabase
using an insert cursor.

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

History:

Christian Wells        09/01/2015               Original coding.

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

Versions Supported:
GDB: All
ArcGIS: 10.1 and above

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

Tags:
WKB, polygon, insert, cursor, binary

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

Resources:
Well-known binary
https://en.wikipedia.org/wiki/Well-known_text#Well-known_binary

InsertCursor
http://desktop.arcgis.com/en/desktop/latest/analyze/arcpy-data-access/insertcursor-class.htm

***********************************************************************/
'''

import struct #Used for reading and packing binary data
import arcpy #Used for interacting with ArcGIS data
import os #Used for interacting with the operating system

#Find a path that the current user has read/write
path = os.path.expanduser('~')

#Create names for the geodatabase and the feature class
gdb_name = 'WKB_Sample.gdb'
fc_name = 'WKB_Polygon'

#Create the geodatabase is if does not exist
if not os.path.exists(os.path.join(path,gdb_name)):
    arcpy.CreateFileGDB_management(path, gdb_name)

#Create the feature class if it does not exist
if not arcpy.Exists(os.path.join(path,gdb_name,fc_name)):
    arcpy.CreateFeatureclass_management(os.path.join(path, gdb_name), fc_name, 'POLYGON', spatial_reference=4326)

#Create a bytearray object to store the well-known binary
wkbarray = bytearray()

#WKB ENDIAN (Little Endian)
endian = struct.pack('b', 1)

#WKB TYPE (Polygon = 3)
wkbtype = struct.pack('i', 3)

#RINGS (Number of Interior/Exterior Rings)
rings = struct.pack('i', 1)

#POINTS (Number of points per ring)
numpoints = struct.pack('i', 4)

#Extend bytearray and fill with data
wkbarray.extend(endian)
wkbarray.extend(wkbtype)
wkbarray.extend(rings)
wkbarray.extend(numpoints)

#Extend bytearray for coordinate 1
wkbarray.extend(struct.pack('d', 0))
wkbarray.extend(struct.pack('d', 0))

#Extend bytearray for coordinate 2
wkbarray.extend(struct.pack('d', 50))
wkbarray.extend(struct.pack('d', 50))

#Extend bytearray for coordinate 3
wkbarray.extend(struct.pack('d', 50))
wkbarray.extend(struct.pack('d', 0))

#Extend bytearray for coordinate 4
wkbarray.extend(struct.pack('d', 0))
wkbarray.extend(struct.pack('d', 0))

#Set feature class variable
fc = os.path.join(path,gdb_name,fc_name)

#Open insert cursor with the shape column, specifiying WKB type
cur = arcpy.da.InsertCursor(fc, ['SHAPE@WKB'])

#Insert the row
cur.insertRow([wkbarray])

#Delete the insert cursor
del cur
