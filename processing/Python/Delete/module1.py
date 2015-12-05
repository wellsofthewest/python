import arcpy

file = r"C:\Incidents\Open\01618800_MXD_Passwords\Water and Sewer Assets.mxd"
oldFile = r"C:\Users\daniela.curl\AppData\Roaming\ESRI\Desktop10.3\ArcCatalog\Connection to GISIII.sde"
newFile = r"Database Connections\Connection to cwells (2).sde"

mxd = arcpy.mapping.MapDocument(file)

for layer in arcpy.mapping.ListLayers(mxd):
    if layer.supports("WORKSPACEPATH") == True:
        layer.findAndReplaceWorkspacePath(oldFile, newFile, False)
        print layer.name

mxd.saveACopy(r"C:\Temp\out.mxd")
