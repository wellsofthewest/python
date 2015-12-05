import arcpy, subprocess, time, getpass, shutil, os

gdb = r"Database Connections\Samu.sde"

instance = "samwow/o1022" #raw_input("Oracle Instance: ")
username = raw_input("SDE Username: ")
password = getpass.getpass("SDE Password: ")

conn = arcpy.ArcSDESQLExecute(instance="sde:oracle11g:{0}".format(instance),user=username,password=password)
fcList = conn.execute("SELECT TABLE_NAME FROM SDE.LAYERS WHERE TABLE_NAME <> 'GDB_ITEMS'")
print fcList

sdeCMD = "sdelayer "
sdeOPT = "-o feature_info "
layerOPT = "-l {0},{1} "
sdeCON = "-i sde:oracle11g:{0} "
sdeUSR = "-u {0} "
sdePSW = "-p {0} "
sdeVAL = "-r invalid"

for fc in fcList:
    print fc[0]
    test = sdeCMD + sdeOPT + sdeCON.format(instance) + sdeUSR.format(username) + sdePSW.format(password) + layerOPT.format(fc[0], "shape") + sdeVAL
    try:
        sqlProc = subprocess.Popen(test, stdout=subprocess.PIPE)
        cmdReturn = sqlProc.communicate()[0]
        print cmdReturn
        cmdReturnFormat = cmdReturn[105:].rstrip()
        resultList = cmdReturnFormat.splitlines()
        total, rows = resultList[-1].split(":")
        if rows.strip() == "0":
            print "None"

        else:
            print "Some"

    except:
        print "dumb"