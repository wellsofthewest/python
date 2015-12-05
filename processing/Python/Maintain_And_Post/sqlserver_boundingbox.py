import arcpy
from arcpy import env

def createSpatialIndexWithBBox(conn, schema_name, fc_name):
    #Get current spatial index name.  
    #Setting the DROP_EXISTING = ON parameter will drop and recreate with the new values
    si_name_sql = "SELECT i.name "
    si_name_sql += "FROM sys.indexes i "
    si_name_sql += "INNER JOIN sys.objects o ON i.object_id = o.object_id "
    si_name_sql += "INNER JOIN sys.schemas sc ON o.schema_id = sc.schema_id "
    si_name_sql += "WHERE o.name = '{}' ".format(fc_name)
    si_name_sql += "AND sc.name = '{}' ".format(schema_name)
    si_name_sql += "AND i.type = 4"
    #print(si_name_sql)
    current_si_name = conn.execute(si_name_sql)
    
    
    get_current_bbox = "SELECT min(((SHAPE.STEnvelope()).STPointN(1)).STX) AS MINX," 
    get_current_bbox += "min(((SHAPE.STEnvelope()).STPointN(1)).STY) AS MINY,"
    get_current_bbox += "max(((SHAPE.STEnvelope()).STPointN(3)).STX) AS MAXX,"
    get_current_bbox += "max(((SHAPE.STEnvelope()).STPointN(3)).STY) AS MAXY " 
    get_current_bbox += "FROM {}.{}".format(schema_name, fc_name)
    
    sde_return = conn.execute(get_current_bbox)
    
    for row in sde_return:
        create_si_ddl = "CREATE SPATIAL INDEX {} ".format(current_si_name)
        create_si_ddl += "ON {}.{}({}) ".format(schema_name, fc_name, spatial_column)
        create_si_ddl += "WITH ( BOUNDING_BOX = ( {}, {}, {}, {} ), ".format(row[0], row[1], row[2], row[3])
        create_si_ddl += "GRIDS = (MEDIUM,MEDIUM,MEDIUM,MEDIUM), "
        create_si_ddl += "DROP_EXISTING = ON );"
        
        try:
            conn.execute(create_si_ddl)
            #print(get_current_bbox)
            print("Success")
        except:
            print("Create index failed")
            print(create_si_ddl)
            

def getAtable(conn, schema_name, fc_name):
    reg_id_sql = "SELECT TOP 1 registration_id FROM sde.sde_table_registry WHERE OWNER = '{}' AND table_name = '{}'".format(schema_name, fc_name)
    reg_id = conn.execute(reg_id_sql)
    a_table_name = "a{}".format(reg_id)
    
    return a_table_name



if __name__ == "__main__":
    #path to SDE connection file
    conn = r"C:\Users\ken6574\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\SUPT00568_CDM_PUB.sde"
    env.workspace = conn
    
    #ArcSDESQLEXECUTE function to open a connection
    sdeConn = arcpy.ArcSDESQLExecute(conn)
    
    #feature class properties
    schema_name = "SDE_LOAD"
    fc_name = "StreetCurb"
    
    desc = arcpy.Describe(fc_name)
    spatial_column = desc.shapeFieldName
    
    if desc.isVersioned != True:
        createSpatialIndexWithBBox(sdeConn, schema_name, fc_name)
    else:
        createSpatialIndexWithBBox(sdeConn, schema_name, fc_name)
        createSpatialIndexWithBBox(sdeConn, schema_name, getAtable(sdeConn, schema_name, fc_name))
