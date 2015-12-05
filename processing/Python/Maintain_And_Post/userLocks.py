import arcpy, os

gdb = r'Database Connections\Barton.sde'

conn = arcpy.ArcSDESQLExecute(gdb)

desc = arcpy.Describe(gdb)
cp = desc.connectionProperties

if cp.user.upper() != 'SDE':
    print 'Connect as the Geodatabase Administrator please'

lockSQL = """SELECT SDE_ID, LOCK_TYPE, LOCK_TIME, 'LAYER' AS LOCK_TBL FROM LAYER_LOCKS
UNION
SELECT SDE_ID, LOCK_TYPE, LOCK_TIME, 'OBJECT' AS LOCK_TBL FROM OBJECT_LOCKS
UNION
SELECT SDE_ID, LOCK_TYPE, LOCK_TIME, 'STATE' AS LOCK_TBL FROM STATE_LOCKS
UNION
SELECT SDE_ID, TO_CHAR(LOCK_TYPE), LOCK_TIME, 'TABLE' AS LOCK_TBL FROM TABLE_LOCKS"""

locks = conn.execute(lockSQL)

for user in arcpy.ListUsers(gdb):
    print '\n{}({})\nConnected from: {}'.format(user.Name, user.ID, user.ClientName)
    for lock in locks:
        if lock[0] == user.ID:
            print '\tLock: {}'.format(lock[3])
            print '\tTime: {}'.format(lock[2])
            print '\tLock Type: {}'.format(lock[2])
            print '\n'



