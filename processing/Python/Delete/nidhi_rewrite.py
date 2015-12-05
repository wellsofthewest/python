import arcpy, os

gdb = r"Database Connections\Connection to cwells.sde"

fields = arcpy.GetParameterAsText(0)
if fields == '#' or not fields:
    fields = "D:\\cases_new\\aaron\\New File Geodatabase.gdb\\fields"

xml_out = arcpy.GetParameterAsText(1)
if xml_out == '#' or not xml_out:
    xml_out = r"C:\temp\fc_xml.xml"

Export_Options = arcpy.GetParameterAsText(2)
if Export_Options == '#' or not Export_Options:
    Export_Options = "DATA" # provide a default value if unspecified


arcpy.ExportXMLWorkspaceDocument_management(fields, xml_out, Export_Options, "BINARY", "METADATA")

arcpy.ImportXMLWorkspaceDocument_management(gdb, xml_out, Export_Options)

