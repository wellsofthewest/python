import arcpy, os

arcpy.env.addOutputsToMap = True
arcpy.env.overwriteOutput = True

mxd = arcpy.mapping.MapDocument("CURRENT")
dataFrame = arcpy.mapping.ListDataFrames(mxd, "*")[0]

def addLayer(lyr, sym):
    lyr_name = os.path.basename(lyr) + "_Layer"
    layer = arcpy.MakeFeatureLayer_management(lyr, lyr_name)
    arcpy.ApplySymbologyFromLayer_management(lyr_name,sym)
    return

def addRaster(lyr, sym):
    lyr_name = os.path.basename(lyr) + "_Raster"
    layer = arcpy.MakeRasterLayer_management(lyr, lyr_name)
    arcpy.ApplySymbologyFromLayer_management(lyr_name, sym)
    return

workspace = "\\KHALEESI\DataStore\Incidents\01683713_GPOutputs\MyWork\datos_visualizar.gdb"
elemento = arcpy.GetParameterAsText(0) # ELEVV1
simbologiaRaster = arcpy.GetParameterAsText(1) #Gotta be a choice list?
simbologyPolygon = r"\\KHALEESI\DataStore\Incidents\01683713_GPOutputs\MyWork\Polygon.lyr"
simbologyPolyline = r"\\KHALEESI\DataStore\Incidents\01683713_GPOutputs\MyWork\Polyline.lyr"
simbologyPoint = r"\\KHALEESI\DataStore\Incidents\01683713_GPOutputs\MyWork\Point.lyr"
simbologyGrayRaster = r"\\KHALEESI\DataStore\Incidents\01683713_GPOutputs\MyWork\RasterStreched.lyr"
simbologyColorRaster = r"\\KHALEESI\DataStore\Incidents\01683713_GPOutputs\MyWork\Composicion.lyr"
simbologyElevationRaster = r"\\KHALEESI\DataStore\Incidents\01683713_GPOutputs\MyWork\Elevacion1.lyr"
simbologiaRasterElev2 = r"\\KHALEESI\DataStore\Incidents\01683713_GPOutputs\MyWork\Elevacion2.lyr"
simbologiaRasterElev3 = r"\\KHALEESI\DataStore\Incidents\01683713_GPOutputs\MyWork\Elevacion3.lyr"
simbologiaRasterTemp = r"\\KHALEESI\DataStore\Incidents\01683713_GPOutputs\MyWork\Temperatura.lyr"
simbologiaRasterPrecip = r"\\KHALEESI\DataStore\Incidents\01683713_GPOutputs\MyWork\Precipitacion.lyr"
simbologiaRasterRV = r"\\KHALEESI\DataStore\Incidents\01683713_GPOutputs\MyWork\RedToGreen.lyr"

if simbologiaRaster == "Polygon":
    simbology = simbologyPolygon
    addLayer(elemento, simbology)
elif simbologiaRaster == "Polyline":
    simbology = simbologyPolyline
    addLayer(elemento, simbology)
elif simbologiaRaster == "Point":
    simbology = simbologyPoint
    addLayer(elemento, simbology)
elif simbologiaRaster == "Escala de Grises":
    simbology = simbologyGrayRaster
    addRaster(elemento, simbology)
elif simbologiaRaster == "Combinacion de color":
    simbology = simbologyColorRaster
    addRaster(elemento, simbology)
elif simbologiaRaster == "Elevacion 1":
    simbology = simbologyElevationRaster
    addRaster(elemento, simbology)
elif simbologiaRaster == "Elevacion 2":
    simbology = simbologiaRasterElev2
    addRaster(elemento, simbology)
elif simbologiaRaster == "Elevacion 3":
    simbology = simbologiaRasterElev3
    addRaster(elemento, simbology)
elif simbologiaRaster == "Temperatura":
    simbology = simbologiaRasterTemp
    addRaster(elemento, simbology)
elif simbologiaRaster == "Precipitacion":
    simbology = simbologiaRasterPrecip
    addRaster(elemento, simbology)
elif simbologiaRaster == "Rojo a Verde":
    simbology = simbologiaRasterRV
    addRaster(elemento, simbology)

