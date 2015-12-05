import pyodbc

conn = pyodbc.connect("DRIVER={SQL SERVER}; SERVER=TOMPSETT; DATABASE=CDM_VectorPub_Prd; UID=sa; PWD=sa")

def query(sql):
    try:
        cursor = conn.cursor() 
        result = cursor.execute(sql)
        return result.fetchall()
    except Exception as err:
        print err

getSi = "SELECT t.name as table_name, idx.name as index_name \
         FROM sys.indexes AS idx INNER JOIN sys.tables t \
         ON t.object_id = idx.object_id \
         WHERE idx.object_id IN (SELECT object_id FROM sys.objects) \
         AND idx.type_desc = 'SPATIAL'"
         
print("Dropping and rebuilding:")
for row in query(getSi):
    print(row[0] + " on " + row[1])
    query("CREATE SPATIAL INDEX {1}\
   ON SDE_LOAD.{0}(shape)\
   WITH ( BOUNDING_BOX = ( -119240500, -96507600, 122521400, 145254300 ), DROP_EXISTING = ON )".format(row[0],row[1]))
    
    
'''
-- Query to get current bounding boxes
SELECT b.name, a.bounding_box_xmin, a.bounding_box_ymin, 
      a.bounding_box_xmax, a.bounding_box_ymax  
FROM sys.spatial_index_tessellations a
INNER JOIN sys.all_objects b
ON
a.object_id = b.object_id
AND b.name IN(SELECT name FROM sys.tables)
order by bounding_box_xmax;
'''