import arcpy, os

arcpy.env.parallelProcessingFactor = "66%"
arcpy.env.overwriteOutput = True

#FGDB Feature Class
streetcl_LOC = r"D:\Scripts\Testing\FHWA_Test.gdb\streetcl2014"
geocode_Results = "D:\Scripts\Testing\FHWA_Test.gdb\Addr_geocoded"
Addr_VDOT = "D:\\Scripts\\Testing\\FHWA_Test.gdb\\Addr_VDOT"

#SDE Feature Class
pubwork_MasterAddr = r"Database Connections\PW_Sandbox.sde\PW_SANDBOX.GISNORFOLK.MASTER_ADDRESS"
parcel_Addr = "Database Connections\\Parcel_RO.sde\\Parcel.GISNORFOLK.Real_Estate\\Parcel.GISNORFOLK.Addresses"
pubwork_CenterLine = "Database Connections\\PublicWorks.sde\\PublicWorks.GISNORFOLK.Transportation\\PublicWorks.GISNORFOLK.street_centerline"


#Views
Addr_VDOT_View = "Addr_VDOT_View"
parcel_Addr_lyr = "Parcel_Addresses_Layer"

# Process: Add Field (2)
arcpy.AddField_management(pubwork_MasterAddr, "FHWA", "TEXT", "", "", "3")

print "add field complete"

# Process: Rebuild Address Locator
arcpy.RebuildAddressLocator_geocoding(streetcl_LOC)

print "rebuild address locator"

# Process: Make Table View
arcpy.MakeTableView_management(parcel_Addr, parcel_Addr_lyr, "STATUS <> 'H'")

print "make table view"

# Process: Geocode Addresses
arcpy.GeocodeAddresses_geocoding(parcel_Addr_lyr, streetcl_LOC, "", geocode_Results, "STATIC")

print "geocode addresses"

# Process: Intersect
arcpy.Intersect_analysis([geocode_Results, pubwork_CenterLine], Addr_VDOT, "NO_FID", "", "INPUT")

print "intersect analysis"

# Process: Make Table View (2)
arcpy.MakeTableView_management(Addr_VDOT, Addr_VDOT_View)

print "make table view"

# Process: Add Field
arcpy.AddField_management(Addr_VDOT_View, "ADDR_FHWA", "TEXT", "", "", "3")

print "add field"

# Process: Calculate Field
codeBlock = """def fhwa(vdot):
 if vdot >=3 and vdot <=5:
  return '{0}'
 else:
  return '{1}'""".format("Yes", "No")

expression = """fhwa( !VDOT!)"""

arcpy.CalculateField_management(Addr_VDOT_View, "ADDR_FHWA", expression, "Python", codeBlock)

print "calculate field"

# Process: Add Attribute Index
arcpy.AddIndex_management(Addr_VDOT_View, "REC_NO", "Addr_index", "NON_UNIQUE", "NON_ASCENDING")

print "add addr_vdotview index"

# Process: Add Join
arcpy.AddJoin_management(pubwork_MasterAddr, "REC_NO", Addr_VDOT_View, "REC_NO", "KEEP_ALL")

print "join tables"

# Calculate Field
codeBlock = """def fhwa(fhwa):
 if fhwa is None:
  return '{0}'
 else:
  return fhwa""".format("No")
expression = """fhwa( !Addr_VDOT.ADDR_FHWA!)"""

arcpy.CalculateField_management(pubwork_MasterAddr, "Publicworks.GISNORFOLK.MASTER_ADDRESS.FHWA", expression, "Python", codeBlock)

print "calculate field"

# Process: Remove Join
arcpy.RemoveJoin_management(pubwork_MasterAddr, "")

print "remove join"

# Process: Add Attribute Index (2)
arcpy.AddIndex_management("", "GPIN", "All_GPINIndex", "NON_UNIQUE", "NON_ASCENDING")

print "model complete"