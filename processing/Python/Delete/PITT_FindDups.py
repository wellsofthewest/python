#Christian Wells
#IMAPS 2013
#
#Name: Find Duplicates in PITT Collection
#
#Purpose: This tool uses the os module to list directories in many root folders.
#Once the directories are listed they are appended to a list. If that value has
#already been attached to the list, it will print the number of the map and
#its location.


import os


completedMaps = r"M:\dep\GIS_Project\PITT\Completed Maps"
digInProgress = r"M:\dep\GIS_Project\PITT\DigInProgress"
georefEscalate = r"M:\dep\GIS_Project\PITT\Georef\Escalate"
noData = r"M:\dep\GIS_Project\PITT\Georef\Escalate\No_Data"
georefInProgress = r"M:\dep\GIS_Project\PITT\Georef\GeorefInProgress"
mine53 = r"M:\dep\GIS_Project\PITT\Georef\GeorefInProgress\Mine_53"
nonUMM = r"M:\dep\GIS_Project\PITT\Georef\Non-UMM"
toGeoref = r"M:\dep\GIS_Project\PITT\Georef\ToGeoref"
mine51 = r"M:\dep\GIS_Project\PITT\Georef\ToGeoref\Mine_51_Sheets-51"
mine52 = r"M:\dep\GIS_Project\PITT\Georef\ToGeoref\Mine_51_Sheets-52"
qcDig = r"M:\dep\GIS_Project\PITT\QC\Digitize"
qcRef = r"M:\dep\GIS_Project\PITT\QC\Georef"
toDig = r"M:\dep\GIS_Project\PITT\ToDigitize"
webPitt = r"M:\web\Georeferenced_SID\PITT"
toDelete = r"M:\dep\GIS_Project\PITT\Georef\ToGeoref\ToDelete"

pittList = []
dupList = []

for a in os.listdir(completedMaps):
    if a not in pittList:
        pittList.append(a)
    else:
        print a + " Completed Maps"

for b in os.listdir(digInProgress):
    if b not in pittList:
        pittList.append(b)
    else:
        print b + " Dig In Progress"

for c in os.listdir(georefEscalate):
    if c not in pittList:
        pittList.append(c)
    else:
        print c + " Escalate"

for d in os.listdir(noData):
    if d not in pittList:
        pittList.append(d)
    else:
        print d + " No Data"

for e in os.listdir(mine53):
    if e not in pittList:
        pittList.append(e)
    else:
        print e + " Mine 53"

for f in os.listdir(georefInProgress):
    if f not in pittList:
        pittList.append(f)
    else:
        print f + " Georef In Progress"

for g in os.listdir(nonUMM):
    if g not in pittList:
        pittList.append(g)
    else:
        print g + " Non UMM"

for h in os.listdir(toGeoref):
    if h not in pittList:
        pittList.append(h)
    else:
        print h + " To Georef"

for i in os.listdir(mine51):
    if i not in pittList:
        pittList.append(i)
    else:
        print i + " Mine 51"

for j in os.listdir(mine52):
    if j not in pittList:
        pittList.append(j)
    else:
        print j + " Mine 52"

for k in os.listdir(qcDig):
    if k not in pittList:
        pittList.append(k)
    else:
        print k + " QC Dig"

for l in os.listdir(qcRef):
    if l not in pittList:
        pittList.append(l)
    else:
        print l + " QC Georef"

for m in os.listdir(toDig):
    if m not in pittList:
        pittList.append(m)
    else:
        print m + " To Dig"

for n in os.listdir(completedMaps):
    if n not in pittList:
        pittList.append(n)
    else:
        print n + " Web Pitt"

for m in os.listdir(toDelete):
    if m not in pittList:
        pittList.append(m)
    else:
        print m + " To Delete"











