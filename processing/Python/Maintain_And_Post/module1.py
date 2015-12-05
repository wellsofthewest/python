import arcpy, subprocess, pyodbc, cx_Oracle, datetime, getpass

instance = raw_input("Oracle Instance: ")
username = raw_input("SDE Username: ")
password = getpass.getpass("SDE Password: ")

conn = cx_Oracle.connect(user='sde', password='sde', dsn=instance)

cmd = """SELECT (L.OWNER || '.' || L.TABLE_NAME) AS OWNER, L.SPATIAL_COLUMN
FROM SDE.LAYERS L JOIN SDE.GDB_ITEMS G ON (L.OWNER || '.' || L.TABLE_NAME) = G.PHYSICALNAME
WHERE G.TYPE IN (SELECT UUID FROM SDE.GDB_ITEMTYPES WHERE NAME='Feature Class')"""

cur = conn.cursor()
cur.execute(cmd)


sdeCMD = "sdelayer "
sdeOPT = "-o feature_info "
layerOPT = """-l {0},{1} """
sdeCON = "-i sde:oracle11g:{0} "
sdeUSR = "-u {0} "
sdePSW = "-p {0} "
sdeVAL = "-r invalid"

resultset = cur.fetchall()
for result in resultset:
    t,s = result
    print t,s
    test = sdeCMD + sdeOPT + sdeCON.format(instance) + sdeUSR.format(username) + sdePSW.format(password) + layerOPT.format(t.lower(), s.lower()) + sdeVAL
    print test
    sqlProc = subprocess.Popen(test, stdout=subprocess.PIPE)
    out = sqlProc.communicate()[0]
    print out[257:-1]



cur.close()
