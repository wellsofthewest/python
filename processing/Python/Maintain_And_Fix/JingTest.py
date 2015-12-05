import arcpy, subprocess, time, getpass, shutil, os

instance = raw_input("Instance: ")
username = raw_input("SDE Username: ")
password = getpass.getpass("SDE Password: ")

conn = arcpy.ArcSDESQLExecute(instance="sde:oracle11g:{0}".format(instance),user=username,password=password)
fcList = conn.execute("SELECT OWNER, TABLE_NAME, SPATIAL_COLUMN FROM SDE.LAYERS WHERE TABLE_NAME <> 'GDB_ITEMS'")

sdeCMD = "sdelayer "
sdeOPT = "-o describe "
layerOPT = "-l {0}.{1},{2} "
sdeCON = "-i sde:oracle11g:{0} "
sdeUSR = "-u {0} "
sdePSW = "-p {0} "

for fc in fcList:
    test = sdeCMD + sdeOPT + sdeCON.format(instance) + sdeUSR.format(username) + sdePSW.format(password) + layerOPT.format(fc[0], fc[1], fc[2])
    try:
        sqlProc = subprocess.Popen(test, stdout=subprocess.PIPE)
        cmdReturn = sqlProc.communicate()[0]
        cmdReturnFormat = cmdReturn[105:].rstrip()
        resultList = cmdReturnFormat.splitlines()
        precision = resultList[11]
        param, value = precision.split(":")
        #print "{0:.<60}: {1}".format(fc[0] + "." + fc[1], value.lstrip())
        if value.lstrip() != 'High':
            print "{0:.<60}: {1}".format(fc[0] + "." + fc[1], value.lstrip())
    except:
        print "Failed to gather precision for feature class: {0}".format(fc[0] + "." + fc[1])
