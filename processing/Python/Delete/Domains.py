# -*- coding: cp1252 -*-
import arcpy
print "hello"

#path to your .sde file with user/password SAVED
gis_workspace = r"C:\Users\matt7099\AppData\Roaming\ESRI\Desktop10.3\ArcCatalog\mziebarth2 sde.sde"

#name of domain you’re looking for
domainName = "Test";

infgdb=(gis_workspace)
arcpy.env.workspace = infgdb

def listfc(inDataset):
    print "checking all feature classes…"
featureclasses = arcpy.ListFeatureClasses("","",inDataset)
for f in featureclasses:
#print "checking feature class: ",f
    lfields=arcpy.ListFields(f)
for lf in lfields:
#if lf.domain > "":
#print "Field",lf.name," domain: ",lf.domain
    if lf.domain == domainName:
        print "!!!found domain applied to: ",f,"–>", lf.name

def listtables():
    print "checking all tables…"
tables = arcpy.ListTables()
for t in tables:
#print "checking table: ",t
    if t != "DIST.PLAN_TABLE":
#Santee Cooper has a bad table to skip
        lfields=arcpy.ListFields(t)
for lf in lfields:
#if lf.domain > "":
#print "Field",lf.name," domain: ",lf.domain
    if lf.domain == domainName:
        print "!!!found domain applied to: ",t,"–>", lf.name

def listds():
    listfc("")
listtables()

#main function
print "checking for domain: ", domainName
listds()

#main function
print "checking for domain: ", domainName
listds()
