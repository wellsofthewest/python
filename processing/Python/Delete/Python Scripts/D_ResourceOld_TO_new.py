##This python Script changes the datasource of an existing mxd and then creates a copy of that mxd
#Import arcpy module
import arcpy

mxd = arcpy.mapping.MapDocument(r"C:\data\1224312\mover.mxd") ##path to existing mxd

newSdePath =r"C:\Users\dami6624\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\SS2nd_sde_tester_dscholzw7.sde" ##new connection file

for lyr in arcpy.mapping.ListLayers(mxd):
    lyr.replaceDataSource(newSdePath, "SDE_WORKSPACE", "", False) 

mxd.saveACopy(r"C:\data\1224312\New_data.mxd") ## Path to new mxd
