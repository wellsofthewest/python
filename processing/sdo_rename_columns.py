import arcpy, os

conn = arcpy.ArcSDESQLExecute(instance='sde:oracle11g:upgrade/stark',
                              user='sde',
                              password='sde')

tblSQL = """SELECT DISTINCT TABLE_NAME FROM USER_TAB_COLS WHERE DATA_TYPE = 'SDO_GEOMETRY'"""
colSQL = """SELECT COLUMN_NAME FROM USER_TAB_COLS WHERE TABLE_NAME = '{0}' AND DATA_TYPE = 'SDO_GEOMETRY'"""
idxSQL = """SELECT C.INDEX_NAME FROM USER_IND_COLUMNS C WHERE C.TABLE_NAME = '{0}' AND C.COLUMN_NAME = '{1}'"""
idxDropSQL = """DROP INDEX {0}"""
tblDropSQL = """ALTER TABLE {0} DROP COLUMN {1}"""
tblRenameSQL = """ALTER TABLE {0} RENAME COLUMN {1} TO {2}"""

tblList = conn.execute(tblSQL)

colNames = ['GDO_GEOMETRY_ORIG', 'GDO_GEOMETRY']
colRename = colNames[0]
colDrop = colNames[1]


def colFunc(tbl):
    colList = conn.execute(colSQL.format(tbl.upper()))
    if isinstance(colList, list):
        return [c[0] for c in colList]
    else:
        return [colList]

if isinstance(tblList, list):
    for tbl in tblList:
        print 'Spatial columns for: {}'.format(tbl[0])
        colList = colFunc(tbl[0])
        for col in colList:
            print '\tColumn: {}'.format(col)
            idx_name = conn.execute(idxSQL.format(tbl[0], col))
            if idx_name <> True and col in colNames:
                conn.execute(idxDropSQL.format(idx_name))
                print '\t\tIndex Dropped: {}'.format(idx_name)
        if colDrop in colList and colRename in colList:
            conn.execute(tblDropSQL.format(tbl[0], colDrop))
            conn.execute(tblRenameSQL.format(tbl[0], colRename, colDrop))
            print '\tColumns renamed'
        if colRename in colList and colDrop not in colList:
            conn.execute(tblRenameSQL.format(tbl[0], colRename, colDrop))
            print '\tColumns renamed'

else:
    print 'Spatial columns for: {}'.format(tbl[0])
    for col in colFunc(tblList):
        print '\tColumn: {}'.format(col)
        idx_name = conn.execute(idxSQL.format(tblList, col))
        if idx_name <> True and col in colNames:
            conn.execute(idxDropSQL.format(idx_name))
            print '\t\tIndex Dropped: {}'.format(idx_name)
    if colDrop in colFunc(tblList) and colRename in colFunc(tblList):
        conn.execute(tblDropSQL.format(tblList, colDrop))
        conn.execute(tblRenameSQL.format(tblList, colRename, colDrop))
        print '\tColumns renamed'
    if colRename in colList and colDrop not in colList:
        conn.execute(tblRenameSQL.format(tblList, colRename, colDrop))
        print '\tColumns renamed'


