import arcpy, os

mxd = arcpy.mapping.MapDocument(r"C:\Incidents\1299591_DDP_Thematic\Test.mxd")
mxdDDP = mxd.dataDrivenPages

for i in arcpy.mapping.ListLayers(mxd):
    i.visible = False

for i in range(mxdDDP.pageCount + 1):
    mxdDDP.currentPageID = i
    name = mxdDDP.pageRow.getValue(mxdDDP.pageNameField.name)
    print name
    if name == 'GEO':
        for i in arcpy.mapping.ListLayers(mxd):
            if i.name == "GEO":
                i.visible = True
                arcpy.RefreshActiveView()
                mxdDDP.exportToPDF(r"C:\temp\GEO.pdf", "CURRENT")
                i.visible = False
                arcpy.RefreshActiveView()
    if name == 'GLA':
        for i in arcpy.mapping.ListLayers(mxd):
            if i.name == "GLA":
                i.visible = True
                arcpy.RefreshActiveView()
                mxdDDP.exportToPDF(r"C:\temp\GLA.pdf", "CURRENT")
                i.visible = False
                arcpy.RefreshActiveView()
    if name == 'PRE':
        for i in arcpy.mapping.ListLayers(mxd):
            if i.name == "PRE":
                i.visible = True
                arcpy.RefreshActiveView()
                mxdDDP.exportToPDF(r"C:\temp\PRE.pdf", "CURRENT")
                i.visible = False
                arcpy.RefreshActiveView()

