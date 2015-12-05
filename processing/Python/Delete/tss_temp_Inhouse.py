import arcpy
from datetime import datetime

sde_path = r'Database Connections\vm2gdb102.sde'
#scratch_gdb = r'C:\miaoer\incidents\1200297\queryTable.gdb'
scratch_gdb = r'C:\incidents\1200297\queryTable.gdb'
sources = ['SDE.AADT_1', 'SDE.LOCATION_1', 'SDE.TxDOT_LOCATION_DYNAMIC_ATTRIBUTE']

where_clause ="SDE.LOCATION_1.LOCAL_ID LIKE \'1%\' and \
SDE.TxDOT_LOCATION_DYNAMIC_ATTRIBUTE.LOCAL_ID = SDE.LOCATION_1.LOCAL_ID \
and SDE.LOCATION_1.LOCAL_ID = SDE.AADT_1.LOCAL_ID"


##sde_path = r'Database Connections\MS2-1200297.sde'
##scratch_gdb = r'C:\incidents\1200297\queryTable.gdb'
##sources = ['DBO.AADT_1', 'DBO.LOCATION', 'DBO.TxDOT_LOCATION_DYNAMIC_ATTRIBUTE']
##
##where_clause = 'DBO.LOCATION.LOCAL_ID LIKE \'1%\' and \
##DBO.TxDOT_LOCATION_DYNAMIC_ATTRIBUTE.LOCAL_ID = DBO.LOCATION.LOCAL_ID \
##and DBO.LOCATION.LOCAL_ID = DBO.AADT_1.LOCAL_ID'

arcpy.env.workspace = sde_path
arcpy.env.overwriteOutput = True


#-----------------------Util--------------------------------
def keep_fieldMapping(source, fld_list):
    fieldMappings = source

    for field in fieldMappings.fields:
        if field.name not in fld_list:
            fieldMappings.removeFieldMap(fieldMappings.findFieldMapIndex(field.name))
            #print field.name + " removed."
    return fieldMappings


def remove_table_prefix(sources, query_table):
    field_mappings = arcpy.FieldMappings()
    field_mappings.addTable(query_table)

    print "remove prefix"
    out_fields = []
    for field in field_mappings.fields:
        #print "field name is:" + field.name
        field_map_index = field_mappings.findFieldMapIndex(field.name)
        field_map = field_mappings.getFieldMap(field_map_index)
        fld_outField = field_map.outputField
        new_field_name = None
        for source in sources:
            try:
                prefix = arcpy.ValidateFieldName(source)
                fld_outField.name.index(prefix)
                new_field_name = fld_outField.name[len(source)+1:]
                break
            except ValueError:
                continue

        if new_field_name not in out_fields:
            fld_outField.name = new_field_name
            fld_outField.aliasName = new_field_name
            if fld_outField.type == 'Integer':
                fld_outField.type = 'Long'
            field_map.outputField = fld_outField
            field_mappings.replaceFieldMap(field_map_index, field_map)
            out_fields.append(fld_outField.name)
        else:
            field_mappings.removeFieldMap(field_map_index)
    return field_mappings


#--------------------------------Main--------------------------------------------------



print "begin make query table..."
ini_time = datetime.now()
query_table = arcpy.MakeQueryTable_management(sources, 'QT', '', '', '', where_clause)

print datetime.now() - ini_time

# Remove the table name prefix in the fields
print "begin remove table prefix..."
field_mapping = remove_table_prefix(sources, query_table)
print datetime.now() - ini_time

# Only kept the fields in this list
keep_fields = ['LATITUDE', 'LONGITUDE', 'STATE_COUNTY_CODE', 'COUNTY', 'PREFIX', 'SITE_NUM', 'SUFFIX']
field_mapping = keep_fieldMapping(field_mapping, keep_fields)

print datetime.now() - ini_time

print "save table to fgdb..."
arcpy.env.overwriteOutput = True
out_table = arcpy.TableToTable_conversion(query_table, sde_path, 'test', '', field_mapping)

print datetime.now() - ini_time
