import arcpy, os, sys
relpath = os.path.dirname(sys.argv[0])

#Read input tool page name
pageName = arcpy.GetParameterAsText(0)

#Reference map document with DDP enabled
mxd = arcpy.mapping.MapDocument(relpath + "\\Sample.mxd")

#Reference data frames
for df in arcpy.mapping.ListDataFrames(mxd):
  if df.name == "MainDF": mainDF = df
  if df.name == "Local Indicator": liDF = df
  if df.name == "Scaled Local Indicator": sliDF = df
  if df.name == "Scaled Indicator": siDF = df
  if df.name == "Global Indicator": giDF = df
  if df.name == "Index2 Indicator": i2iDF = df

#Set extent of Main DF (via DDP)
pageID = mxd.dataDrivenPages.getPageIDFromName(pageName)
mxd.dataDrivenPages.currentPageID = pageID

#Set extent of Local Indicator DF
lyr = arcpy.mapping.ListLayers(mxd, "US_States", liDF)[0]
query = "State_Name = '" + pageName + "'"
arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", query)
arcpy.SelectLayerByLocation_management(lyr, "BOUNDARY_TOUCHES", lyr)
newExt = lyr.getSelectedExtent()
liDF.extent = newExt
arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION")

#Set extent of Local Indicator DF
lyr = arcpy.mapping.ListLayers(mxd, "US_States", sliDF)[0]
query = "State_Name = '" + pageName + "'"
arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", query)
newExt = lyr.getSelectedExtent()
sliDF.extent = newExt
sliDF.scale = liDF.scale * 0.75
arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION")

#Set extent of Scaled Indicator DF
lyr = arcpy.mapping.ListLayers(mxd, "US_States", siDF)[0]
query = "State_Name = '" + pageName + "'"
arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", query)
newExt = lyr.getSelectedExtent()
siDF.extent = newExt
siDF.scale = liDF.scale * 0.50
arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION")

#Set extent for Global Indicator
newExt = lyr.getExtent()
giDF.extent = newExt

#Set extent for Index2 Indicator
regionName = mxd.dataDrivenPages.pageRow.getValue("SUB_REGION")
query = "SUB_REGION = '" + regionName + "'"
lyr = arcpy.mapping.ListLayers(mxd, "US_States_Dis", i2iDF)[0]
arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", query)
newExt = lyr.getSelectedExtent()
i2iDF.extent = newExt
arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION")

#Export to PDF and open
arcpy.mapping.ExportToPDF(mxd, relpath + "\\output.pdf")
os.startfile(relpath + "\\output.pdf")


