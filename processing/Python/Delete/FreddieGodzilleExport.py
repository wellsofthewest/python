import arcpy, os, string
from arcpy import env as e
from os import path as p

# Environment
e.overwriteOutput = True

# Data: Collect inputs from GP Tool
feat = r"C:\Users\chri0000\Documents\ArcGIS\Default.gdb\Richland"
fnet = r"C:\Users\chri0000\Documents\ArcGIS\Default.gdb\GodzillaExport2"

# Process: Get the name of the ObjectID field in the feature class
OIDF = arcpy.Describe(fnet).OIDfieldname

# Process: Create a search cursor object
rows = arcpy.SearchCursor(dataset=fnet, fields=OIDF)

# Data: Local variables
cntr = 0
totl = arcpy.GetCount_management(fnet).getOutput(0)

for row in rows:
    
    # Process: Increment the counter by one
    cntr += 1
    arcpy.AddMessage("Processing GRID %s of %s" % (cntr, totl))
    
    # Process: Get the current Object from the current row
    OID = row.getValue(OIDF)
    
    # Process: Create a feature layer for the current row of the cursor
    lyr = arcpy.MakeFeatureLayer_management(fnet, "layer", "\"%s\" = %s" % (OIDF, OID))
    
    # Environment: Restrict the processing extent to that of the current layer
    e.extent = arcpy.Describe(lyr).extent
    print e.extent
    
    try:
        
        # Process: Clip the feature to the current layer
        arcpy.AddMessage("  Clipping current GRID...")
        GDB = p.dirname(feat)
        CLP = p.join(GDB, "CLPResult%s" % str(OID).zfill(2))
        arcpy.Clip_analysis(feat, lyr, CLP)
        
        if int(arcpy.GetCount_management(CLP).getOutput(0)):
            # Process: Export the clipped layer to CAD
            arcpy.AddMessage("  Exporting feature to CAD...")
            FOL = p.join(p.dirname(GDB), "CAD_OUTPUT")
            if not p.exists(FOL):
                os.mkdir(FOL)
            CAD = p.join(FOL, "CADResult%s.dwg" % str(OID).zfill(2))
            arcpy.ExportCAD_conversion(CLP, "DWG_R2010", CAD)
            arcpy.AddMessage("    CAD Result is %s" % CAD)
        else:
            arcpy.AddMessage("  GRID was empty...continuing to next GRID")
            arcpy.Delete_management(CLP)
    
    except:
        arcpy.AddMessage("  ** Error processing feature **")
    
    del lyr, OID
    
del row, rows
