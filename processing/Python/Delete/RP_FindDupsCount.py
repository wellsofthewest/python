#Christian Wells
#IMAPS 2013
#
#Name: Find Duplicates and Counts in RP Collection
#
#Purpose: This tool uses the os module to list directories in many root folders.
#Once the directories are listed they are appended to a list. If that value has
#already been attached to the list, it will print the number of the map and
#its location. In addition it provides a total count of all the maps in the
#listed directories.

import os

web = os.listdir(r"M:\web\Georeferenced_SID")
dig = os.listdir(r"M:\dep\GIS_Project\Digitization")
QCNoData = os.listdir(r"M:\dep\GIS_Project\GeorefSID\NO_DATA")
QCNonUMM = os.listdir(r"M:\dep\GIS_Project\GeorefSID\NON_UMM")
QCGeoref = os.listdir(r"M:\dep\GIS_Project\GeorefSID\QC_Georef\NEED_FIXED")
QCGeorefNON = os.listdir(r"M:\dep\GIS_Project\GeorefSID\QC_Georef\NON_UMM")

CountList = []

for i in web:
    if i not in CountList:
        CountList.append(i)
    else:
        print "web/" +i
for i in dig:
    if i not in CountList:
        CountList.append(i)
    else:
        print "dig/" +i

for i in QCNoData:
    if i not in CountList:
        CountList.append(i)
    else:
        print "GeorefNoData/" +i

for i in QCNonUMM:
    if i not in CountList:
        CountList.append(i)
    else:
        print "NON_UMM/" +i

for i in QCGeoref:
    if i not in CountList:
        CountList.append(i)
    else:
        print "NEEDFIXED/" +i

for i in QCGeorefNON:
    if i not in CountList:
        CountList.append(i)
    else:
        print "GeorefNONUMM/" +i

print len(CountList)

print CountList



