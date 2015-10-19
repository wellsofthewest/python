import arcpy, os

gdb = r'Database Connections\stark.sde'

arcpy.env.workspace = gdb

conn = arcpy.ArcSDESQLExecute(gdb)

sql_reg = "SELECT REGISTRATION_ID FROM TABLE_REGISTRY WHERE OWNER = '{0}' AND TABLE_NAME = '{1}'"
sql_lyr = "SELECT LAYER_ID, SPATIAL_COLUMN, SRID FROM LAYERS WHERE OWNER = '{0}' AND TABLE_NAME = '{1}'"
sql_typ = "SELECT DATA_TYPE FROM USER_TAB_COLS WHERE TABLE_NAME = '{0}' AND COLUMN_NAME = '{1}'"
sql_idx = "SELECT COUNT(*) FROM USER_INDEXES WHERE TABLE_OWNER = '{0}' AND TABLE_NAME = '{1}' AND ITYP_NAME in ('SPATIAL_INDEX', 'ST_SPATIAL_INDEX')"
idx_b = 'CREATE INDEX {0}.A{1}_IX1 ON {0}.{2}({3}) INDEXTYPE IS MDSYS.SPATIAL_INDEX'
idx_a = 'CREATE INDEX {0}.A{1}_IX1_A ON {0}.A{2}({3}) INDEXTYPE IS MDSYS.SPATIAL_INDEX'
idx_b_st = "CREATE INDEX {0}.A{1}_IX1 ON {0}.{2}({3}) INDEXTYPE IS sde.st_spatial_index parameters ('st_grids={4},{5},{6} st_srid={7}')"
idx_a_st = "CREATE INDEX {0}.A{1}_IX1_A ON {0}.A{2}({3}) INDEXTYPE IS sde.st_spatial_index parameters ('st_grids={4},{5},{6} st_srid={7}')"
get_srid = "SELECT AUTH_SRID FROM SPATIAL_REFERENCES WHERE SRID = {0}"

for dir, dirpath, files in arcpy.da.Walk(gdb):
    for file in files:
        path = os.path.join(dir,file)
        desc = arcpy.Describe(path)
        if desc.isVersioned == True and desc.datasetType == 'FeatureClass' and desc.DSID >= 0:
            owner, table = file.split('.')
            reg_id = conn.execute(sql_reg.format(owner.upper(), table.upper()))
            lyr = conn.execute(sql_lyr.format(owner.upper(), table.upper()))
            sp_col = conn.execute(sql_typ.format(table.upper(), lyr[0][1].upper()))
            SRID = conn.execute(get_srid.format(lyr[0][2]))
            if sp_col == 'SDO_GEOMETRY':
                base_idx_status = conn.execute(sql_idx.format(owner.upper(), table.upper()))
                adds_idx_status = conn.execute(sql_idx.format(owner.upper(), 'A{}'.format(reg_id).upper()))
                print '{}: Checking for spatial indexes...'.format(file)
                if int(base_idx_status) == 0:
                    conn.execute(idx_b.format(owner, lyr[0][0], table, lyr[0][1]))
                    print '{}: Spatial index added to base'.format(file)
                if int(base_idx_status) == 1:
                    print '{}: Spatial index exists on base'.format(file)

                if int(adds_idx_status) == 0:
                    conn.execute(idx_a.format(owner, lyr[0][0], reg_id, lyr[0][1]))
                    print '{}: Spatial index added to adds'.format(file)
                if int(adds_idx_status) == 1:
                    print '{}: Spatial index exists on adds'.format(file)
            if sp_col == 'ST_GEOMETRY':
                base_idx_status = conn.execute(sql_idx.format(owner.upper(), table.upper()))
                adds_idx_status = conn.execute(sql_idx.format(owner.upper(), 'A{}'.format(reg_id).upper()))
                print '{}: Checking for spatial indexes...'.format(file)
                results = arcpy.CalculateDefaultGridIndex_management(path)
                if int(base_idx_status) == 0:
                    conn.execute(idx_b_st.format(owner, lyr[0][0], table, lyr[0][1], results[0], results[1], results[2], SRID))
                    print '{}: Spatial index added to base'.format(file)
                if int(base_idx_status) == 1:
                    print '{}: Spatial index exists on base'.format(file)

                if int(adds_idx_status) == 0:
                    conn.execute(idx_a_st.format(owner, lyr[0][0], reg_id, lyr[0][1], results[0], results[1], results[2], SRID))
                    print '{}: Spatial index added to adds'.format(file)
                if int(adds_idx_status) == 1:
                    print '{}: Spatial index exists on adds'.format(file)


        if desc.isVersioned == False and desc.datasetType == 'FeatureClass' and desc.DSID >= 0:
            owner, table = file.split('.')
            reg_id = conn.execute(sql_reg.format(owner.upper(), table.upper()))
            lyr = conn.execute(sql_lyr.format(owner.upper(), table.upper()))
            sp_col = conn.execute(sql_typ.format(table.upper(), lyr[0][1].upper()))
            SRID = conn.execute(get_srid.format(lyr[0][2]))
            if sp_col == 'SDO_GEOMETRY':
                base_idx_status = conn.execute(sql_idx.format(owner.upper(), table.upper()))
                print '{}: Checking for spatial indexes...'.format(file)
                if int(base_idx_status) == 0:
                    conn.execute(idx_b.format(owner, lyr[0][0], table, lyr[0][1]))
                    print '{}: Spatial index added to base'.format(file)
                if int(base_idx_status) == 1:
                    print '{}: Spatial index exists on base'.format(file)
            if sp_col == 'ST_GEOMETRY':
                base_idx_status = conn.execute(sql_idx.format(owner.upper(), table.upper()))
                print '{}: Checking for spatial indexes...'.format(file)
                results = arcpy.CalculateDefaultGridIndex_management(path)
                if int(base_idx_status) == 0:
                    conn.execute(idx_b_st.format(owner, lyr[0][0], table, lyr[0][1], results[0], results[1], results[2], SRID))
                    print '{}: Spatial index added to base'.format(file)
                if int(base_idx_status) == 1:
                    print '{}: Spatial index exists on base'.format(file)
