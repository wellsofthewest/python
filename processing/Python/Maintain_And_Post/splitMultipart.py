import arcpy

conn = arcpy.ArcSDESQLExecute(r'Database Connections\Connection to justinm.sde')

sql_parts = 'select sde.st_numgeometries(shape) as numparts, objectid from anno6'

shpList = conn.execute(sql_parts)

genCent = 'insert into explode_anno (row_id, orig_oid, orig_shape, shape_parts, x_coord, y_coord) select {0}, objectid, sde.st_astext(shape), sde.st_centroid(sde.st_geometryn(shape, {1})), sde.st_x(sde.st_centroid(sde.st_geometryn(shape, {1}))), sde.st_y(sde.st_centroid(sde.st_geometryn(shape, {1}))) from anno6 where objectid = {2}'
nullCent = 'insert into explode_anno (row_id, orig_oid, orig_shape, shape_parts, x_coord, y_coord) select {0}, objectid, null, null, null, null from anno6 where objectid = {2}'
cnt = 1
for shp in shpList:
    for x in range(1, int(shp[0])+1):
        try:
            conn.execute(genCent.format(cnt, x, shp[1]))
        except:
            conn.execute(nullCent.format(cnt,x,shp[1]))
        cnt+=1


