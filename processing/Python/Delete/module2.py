import arcpy, subprocess, cx_Oracle, time, getpass, shutil, os

userHome = os.path.expanduser("~")
workPath = os.path.join(userHome, "SDETest")

if os.path.exists(workPath) == False:
    os.mkdir(workPath)

outLog = open(os.path.join(workPath, "LogFile.txt"), "w+")

instance = raw_input("Oracle Instance: ")
username = raw_input("SDE Username: ")
password = getpass.getpass("SDE Password: ")

conn = cx_Oracle.connect(user=username, password=password, dsn=instance)

cmd = """SELECT (L.OWNER || '.' || L.TABLE_NAME) AS PHYSICALNAME, L.SPATIAL_COLUMN, T.ROWID_COLUMN, T.REGISTRATION_ID,
CASE WHEN (A.ARCHIVING_REGID > 0) THEN 'true' ELSE 'false' END AS ARCHIVED
FROM LAYERS L JOIN GDB_ITEMS_VW G
ON (L.OWNER || '.' || L.TABLE_NAME) = G.PHYSICALNAME
JOIN SDE.TABLE_REGISTRY T ON G.PHYSICALNAME = (T.OWNER || '.' || T.TABLE_NAME)
LEFT JOIN SDE_ARCHIVES A ON A.ARCHIVING_REGID = T.REGISTRATION_ID
WHERE G.TYPE IN (SELECT UUID FROM GDB_ITEMTYPES WHERE NAME='Feature Class')
AND L.TABLE_NAME IN (SELECT TABLE_NAME FROM ALL_TAB_COLS WHERE DATA_TYPE='SDO_GEOMETRY') ORDER BY 1"""

cur = conn.cursor()
cur.execute(cmd)

oraFail = []
sdoFail = []
sdeFail = []
infFail = []
sdeCMD = "sdelayer "
sdeOPT = "-o feature_info "
layerOPT = "-l {0},{1} "
sdeCON = "-i sde:oracle11g:{0} "
sdeUSR = "-u {0} "
sdePSW = "-p {0} "
sdeVAL = "-r invalid"

sdoVAL = """SELECT A.{0}
FROM  {1} A,
USER_SDO_GEOM_METADATA M
WHERE M.table_name = '{2}'
AND M.column_name = '{3}'
AND SDO_GEOM.VALIDATE_GEOMETRY_WITH_CONTEXT(A.{3}, M.diminfo) <> 'TRUE'"""

sdoVAL_A = """SELECT A.{0}
FROM  {1}.A{4} A,
USER_SDO_GEOM_METADATA M
WHERE M.table_name = 'A{2}'
AND M.column_name = '{3}'
AND SDO_GEOM.VALIDATE_GEOMETRY_WITH_CONTEXT(A.{3}, M.diminfo) <> 'TRUE'"""

sdoVAL_H = """SELECT A.{0}
FROM  {1}_H A,
USER_SDO_GEOM_METADATA M
WHERE M.table_name = '{2}_H'
AND M.column_name = '{3}'
AND SDO_GEOM.VALIDATE_GEOMETRY_WITH_CONTEXT(A.{3}, M.diminfo) <> 'TRUE'"""

verREG = """select gdb_util.is_versioned('{0}','{1}') FROM DUAL"""

addTBL = "{0}.A{1}"
arcTBL = "{0}.{1}_H"

resultset = cur.fetchall()

outLog.write("\n\nSDO Feature Classes within the geodatabase:\n")

for result in resultset:
    physicalname,shape,rowid, regid, arcBool = result
    own,table_name = physicalname.split(".")
    outLog.write("\n{0:12}{1:30}".format(own, table_name))

for result in resultset:
    physicalname,shape,rowid, regid, arcBool = result
    own,table_name = physicalname.split(".")
    test = sdeCMD + sdeOPT + sdeCON.format(instance) + sdeUSR.format(username) + sdePSW.format(password) + layerOPT.format(physicalname.lower(), shape.lower()) + sdeVAL
    print "\nScanning the following feature class for invalid objects: {0}".format(physicalname)
    outLog.write("\n\nScanning the following feature class for invalid objects: {0}".format(physicalname))

    outLog.write("\nOracle SDO Validate with Context Scan:")

    cur.execute(verREG.format(own,table_name))
    versionedset = cur.fetchall()
    for ver in versionedset:
        verBool = ver[0]


    try:
        cur.execute(sdoVAL.format(rowid, physicalname, table_name, shape))
        invalidset = cur.fetchall()
        if len(invalidset) > 0:
            sdoFail.append(physicalname)
            for invalid in invalidset:
                outLog.write("\nSDO Invalid Geometries: {0}".format(invalid))

        else:
            outLog.write("\n\tNo invalid SDO features found")

        if verBool.upper() == 'TRUE':
            outLog.write("\nOracle SDO Validate with Context Scan for the adds table:")
            try:
                cur.execute(sdoVAL_A.format(rowid, own, table_name, shape, regid))
                invalidset = cur.fetchall()
                if len(invalidset) > 0:
                    sdoFail.append(addTBL.format(own,regid))
                    for invalid in invalidset:
                        outLog.write("\nSDO Invalid Geometries: {0}".format(invalid))
                else:
                    outLog.write("\n\tNo invalid SDO features found")

            except:
                oraFail.append(addTBL.format(own,regid))
                outLog.write("\n\tFailed to scan the adds table for validity")

        if verBool.upper() == 'FALSE':
            outLog.write("\n\tFeature class not registered as versioned, no SDO validation required on delta tables")

        if arcBool.upper() == 'TRUE' and verBool.upper() == 'TRUE':
            outLog.write("\nOracle SDO Validate with Context Scan for the archiving table:")

            try:
                cur.execute(sdoVAL_H.format(rowid, physicalname, table_name, shape))
                invalidset = cur.fetchall()
                if len(invalidset) > 0:
                    sdoFail.append(arcTBL.format(own,table_name))
                    for invalid in invalidset:
                        outLog.write("\nSDO Invalid Geometries: {0}".format(invalid))
                else:
                    outLog.write("\n\tNo invalid SDO features found")

            except:
                oraFail.append(arcTBL.format(own,table_name))
                outLog.write("\n\tFailed to scan the archiving table for validity")

        if arcBool.upper() == 'FALSE':
            outLog.write("\n\tFeature class not enabled for archiving, no SDO validation required on archiving tables")


    except:
        oraFail.append(physicalname)
        outLog.write("\n\tFailed to scan the following feature class for validity: {0}".format(physicalname))



    outLog.write("\n\nArcSDE sdelayer -o feature_info results:")
    try:
        sqlProc = subprocess.Popen(test, stdout=subprocess.PIPE)
        cmdReturn = sqlProc.communicate()[0]
        cmdReturnFormat = cmdReturn[105:].rstrip()
        resultList = cmdReturnFormat.splitlines()
        total, rows = resultList[-1].split(":")
        if rows.strip() == "0":
            outLog.write("\n\tNo invalid features found")
            outLog.write("\n\t" + resultList[-2])
            outLog.write("\n\t" + resultList[-1])
        else:
            infFail.append(physicalname)
            outLog.write("\n\tInvalid features have been found, returning invalid objects...")
            outLog.write(cmdReturnFormat)
    except:
        sdeFail.append(physicalname)
        outLog.write("\n\tFailed to open the following feature class: {0}".format(physicalname))


oraFail.sort()
sdoFail.sort()
sdeFail.sort()
infFail.sort()

if len(oraFail) > 0:
    outLog.write("\n\n\nThe following SDO tables failed to validate with context:")
    for fail in oraFail:
        print fail
        outLog.write("\n"+fail)

else:
    outLog.write("\n\n\nAll SDO tables validated with context")

if len(sdeFail) > 0:
    outLog.write("\n\n\nThe following feature classes failed to open with sdelayer -o feature_info:")
    for fail in sdeFail:
        print fail
        outLog.write("\n"+fail)

else:
    outLog.write("\n\n\nAll feature classes opened with sdelayer -o feature_info")


if len(sdoFail) > 0:
    outLog.write("\n\n\nThe following SDO tables have invalid geometries")
    for fail in sdoFail:
        print fail
        outLog.write("\n"+fail)

if len(infFail) > 0:
    outLog.write("\n\n\nThe following feature classes have invalid features per sdelayer -o feature_info")
    for fail in infFail:
        print fail
        outLog.write("\n"+fail)


cur.close()
outLog.close()

print "\n\nCompleted"
print "\n\nPlease delete the following directory upon resolution:\n{0}".format(workPath)
time.sleep(10)
os.startfile(os.path.join(workPath, "LogFile.txt"))
