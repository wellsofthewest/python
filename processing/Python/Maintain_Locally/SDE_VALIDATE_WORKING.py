import arcpy, subprocess, time, getpass, shutil, os, sys

dbmsType = ""
dbms = raw_input("RDBMS: ")
dbms = dbms.replace(' ', '')
if dbms.upper() == "ORACLE":
    oraVer = raw_input("Oracle Version [ex. 10, 11, 12]: ")
    if oraVer.strip() == '10':
        dbmsType = "oracle10g"
    if oraVer.strip() == '11':
        dbmsType = "oracle11g"
    if oraVer.strip() == '12':
        dbmsType = "oracle11g"
    instance = raw_input("Instance: ")
    username = raw_input("SDE Username: ")
    password = getpass.getpass("SDE Password: ")
    conn = arcpy.ArcSDESQLExecute(instance="sde:{0}:{1}".format(dbmsType,instance),user=username,password=password)
    fcList = conn.execute("SELECT TABLE_NAME,SPATIAL_COLUMN,OWNER FROM SDE.LAYERS WHERE TABLE_NAME <> 'GDB_ITEMS' AND OWNER = '{0}'".format(username.upper()))
    if fcList == True:
        print "No data is owned by: {0}".format(username.upper())
        sys.exit(0)
    sdeCMD = "sdelayer -o feature_info -l {0},{1} -i sde:{2}:{3} -u {4} -p {5} -r invalid"
    for fc in fcList:
        try:
            cmd = sdeCMD.format(fc[0], fc[1], dbmsType, instance, username, password)
            sqlProc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            cmdReturn = sqlProc.communicate()[0]
            cmdReturnFormat = cmdReturn[105:].rstrip()
            resultList = cmdReturnFormat.splitlines()
            total, rows = resultList[-1].split(":")
            if rows.strip() == "0":
                print "\n\n" + str(fc[0]) + ": VALID"
                print resultList[-2]
                print resultList[-1]
            else:
                print "\n\n" + str(fc[0]) + ": INVALID"
                print cmdReturnFormat

        except:
            print "Command Failed for feature class: {0}".format(fc[0])



if dbms.upper() == "SQLSERVER":
    dbmsType = "sqlserver"
    instance = raw_input("Instance: ")
    dbName = raw_input("Database Name: ")
    username = raw_input("SDE Username: ")
    password = getpass.getpass("SDE Password: ")
    conn = arcpy.ArcSDESQLExecute(instance="sde:{0}:{1}".format(dbmsType,instance),database=dbName,user=username,password=password)
    fcList = conn.execute("SELECT TABLE_NAME,SPATIAL_COLUMN FROM SDE.SDE_LAYERS WHERE TABLE_NAME <> 'GDB_ITEMS' AND OWNER = '{0}'".format(username.upper()))
    sdeCMD = "sdelayer -o feature_info -l {0},{1} -i sde:{2}:{3} -u {4} -p {5} -D {6} -r invalid"
    if fcList == True:
        print "No data is owned by: {0}".format(username.upper())
        sys.exit(0)
    for fc in fcList:
        try:
            cmd = sdeCMD.format(fc[0], fc[1], dbmsType, instance, username, password, dbName)
            sqlProc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            cmdReturn = sqlProc.communicate()[0]
            cmdReturnFormat = cmdReturn[105:].rstrip()
            resultList = cmdReturnFormat.splitlines()
            total, rows = resultList[-1].split(":")
            if rows.strip() == "0":
                print "\n\n" + str(fc[0]) + ": VALID"
                print resultList[-2]
                print resultList[-1]
            else:
                print "\n\n" + str(fc[0]) + ": INVALID"
                print cmdReturnFormat

        except:
            print "Command Failed for feature class: {0}".format(fc[0])


time.sleep(20)