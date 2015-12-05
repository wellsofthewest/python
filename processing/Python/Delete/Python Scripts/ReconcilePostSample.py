OracleInstance = "SDED"
lines = ""
#workspace = "B:/Public/GIS/Service/Database Connections/" + OracleInstance+ "_SDE.sde"
workspace = r"C:\share\DatabaseConnections\Oracle\CWELLS101@CWELLS@ORACLE@SDE.sde"
versions = arcpy.da.ListVersions(workspace)

# Variables: log file, counters for conflict and error
sCode = 0
lines = ""
cCount = 0
eCount = 0
verCnt = 0

# Report file name and locations
#reportTime = datetime.datetime.now().strftime("%Y-%m-%d")
dTime = time.strftime('%Y-%m-%d_%H%M')
#file = "F:/GIS/Logs/AutoReconcile/Reconcile_" + OracleInstance+ "_%s.txt" %dTime
file = r"C:\Incidents\Phoenix\test.txt"
#recFolder = r"F:\GIS\Logs\AutoReconcile\ReconcileDetailLogs"
recFolder = r"C:\Incidents\Phoenix\RecLogs"
try:
    for i in os.listdir(recFolder):
        os.remove(os.path.join(recFolder,i))
except:
    print "Cannot delete files from " + recFolder

#Create and open report file in writing mode
text_file=open(file,"w")

# Lines for output report
lines = ["Reconcile result: \n "]
lines.append("Started at " + time.strftime('%X %x') + "\n")

#Loop through version list
versionList = []
verList = []
remList = []
for version in versions:
    if version.name != "SDE.DEFAULT":
        verList.append(version.name)
        remList.append(version.name)
for version in versions:
    if version.parentVersionName == "SDE.DEFAULT":
        childList = []
        verCnt += 1
        versionList.append(version.name)
        remList.remove(version.name)
        verName = version.name.replace(".","_")
        for child in version.children:
            childList.append(child.name)
            verCnt += 1
            remList.remove(child.name)
            childName = child.name.replace(".","_")
        if len(childList) > 0:
            try:
                #arcpy.ReconcileVersions_management(workspace,"ALL_VERSIONS",version.name,childList,"LOCK_ACQUIRED","NO_ABORT","BY_OBJECT","FAVOR_TARGET_VERSION","NO_POST","KEEP_VERSION",os.path.join(recFolder,"Reconcile_" + verName + "_" + OracleInstance+ "_%s.txt" %dTime))
                arcpy.ReconcileVersions_management(workspace,"ALL_VERSIONS",version.name,childList,"LOCK_ACQUIRED","NO_ABORT","BY_OBJECT","FAVOR_TARGET_VERSION","NO_POST","KEEP_VERSION",os.path.join(recFolder,"Reconcile_" + verName + "_" + OracleInstance + "_%s.txt" %dTime))
                lines.append("Reconcile of " + version.name + " children succeeded \n")
            except Exception as e:
                resultStr = "\n A conflict detected under the version " + version.name + " and children" + "\n"
                cCount +=1
                verCnt -= 1
                print "A conflict detected under the version " + version.name
                lines.append(str(resultStr))
                lines.append(str(arcpy.GetMessages(2)))
        for child in version.children:
            gChildList = []
            for gChild in child.children:
                gChildList.append(gChild.name)
                verCnt += 1
                remList.remove(gChild.name)
                ChildName = child.name.replace(".","_")
            if len(gChildList) > 0:
                try:
                    print workspace, child.name, gChildList
                    #arcpy.ReconcileVersions_management(r'Database Connections\SDED_SDE.sde',"ALL_VERSIONS","PREACCPT.VERSIONCHILD2","SDE.GGChild","LOCK_ACQUIRED","NO_ABORT","BY_OBJECT","FAVOR_TARGET_VERSION","NO_POST","KEEP_VERSION",os.path.join(recFolder,"Reconcile_" + gChildName + "_" + OracleInstance+ "_%s.txt" %dTime))
                    arcpy.ReconcileVersions_management(workspace,"ALL_VERSIONS",child.name,gChildList,"LOCK_ACQUIRED","NO_ABORT","BY_OBJECT","FAVOR_TARGET_VERSION","NO_POST","KEEP_VERSION",os.path.join(recFolder,"Reconcile_" + ChildName + "_" + OracleInstance + "_%s.txt" %dTime))
                    lines.append("Reconcile of " + child.name + " children succeeded \n")
                except Exception as e:
                    resultStr = "\n A conflict detected under the version " + child.name + " and children" + "\n"
                    cCount +=1
                    verCnt -= 1
                    print "A conflict detected under the version2 " + child.name
                    lines.append(str(resultStr))
                    lines.append(str(arcpy.GetMessages(2)))
for remVersion in versions:
    if remVersion.name in remList:
        verCnt += 1
        remList.remove(remVersion.name)
        remName = remVersion.parentVersionName.replace(".","_")
        try:
            #arcpy.ReconcileVersions_management(workspace,"ALL_VERSIONS",remVersion.parentVersionName,remVersion.name,"LOCK_ACQUIRED","NO_ABORT","BY_OBJECT","FAVOR_TARGET_VERSION","NO POST","KEEP_VERSION",os.path.join(recFolder,"Reconcile_" + remVersion.name + "_" + OracleInstance+ "_%s.txt" %dTime))
            arcpy.ReconcileVersions_management(workspace,"ALL_VERSIONS",remVersion.parentVersionName,remVersion.name,"LOCK_ACQUIRED","NO_ABORT","BY_OBJECT","FAVOR_TARGET_VERSION","NO_POST","KEEP_VERSION",os.path.join(recFolder,"Reconcile_" + remName + "_" + OracleInstance + "_%s.txt" %dTime))
            lines.append("Reconcile of " + remVersion.parentVersionName + " children succeeded \n")
        except Exception as e:
           resultStr = "\n A error occurred while reconciling with the " + remVersion.parentVersionName + " version \n"
           detail = "Error detected, Please see the log file ( " + file + " ) for information"
           status = "ERROR"
           cCount +=1
           verCnt -= 1
           lines.append(str(resultStr))
           lines.append(str(arcpy.GetMessages(2)))
try:
   #arcpy.ReconcileVersions_management(workspace,"ALL_VERSIONS","SDE.DEFAULT",versionList,"LOCK_ACQUIRED","NO_ABORT","BY_OBJECT","FAVOR_TARGET_VERSION","POST","KEEP_VERSION",os.path.join(recFolder,"Reconcile_SDE_DEFAULT_" + OracleInstance+ "_%s.txt" %dTime))
   arcpy.ReconcileVersions_management(workspace,"ALL_VERSIONS","SDE.DEFAULT",versionList,"LOCK_ACQUIRED","NO_ABORT","BY_OBJECT","FAVOR_TARGET_VERSION","POST","KEEP_VERSION",os.path.join(recFolder,"Reconcile_SDE_DEFAULT_" + OracleInstance + "_%s.txt" %dTime))
   lines.append("Reconcile of SDE_DEFAULT children succeeded \n")

except Exception as e:
   resultStr = "\n A error occurred while reconciling with the SDE_DEFAULT version \n"
   detail = "Error detected, Please see the log file ( " + file + " ) for information"
   status = "ERROR"
   cCount +=1
   verCnt -= 1
   print "RECONCILE           ERROR", #OracleInstance, e
   lines.append(str(resultStr))
   lines.append(str(arcpy.GetMessages(2)))

finally:
    #print len(verList)
    #print verCnt
    #print remList

    if len(verList) == verCnt:
       print "All versions reconciled"
    else:
       print "All versions were not reconciled"
    # Write log file
    lines.append("\nEnded at " + time.strftime('%X %x') + "\n")
    text_file.writelines(lines)
    text_file.close()
    '''

    # Send Email
    #emailFrom = 'mapservices@phoenix.gov'
    #emailTo = ['mapservices@phoenix.gov']
    #emailCC = ['mapservices@phoenix.gov']
    emailFrom = 'james.jarvis@phoenix.gov'
    emailTo = ['james.jarvis@phoenix.gov']
    emailCC = ['james.jarvis@phoenix.gov']

    # Write to log talbe in SQL server
    if (cCount <= 0 and eCount <= 0):
        detail ="Completed successfully"
        status = "END"

    elif (cCount > 0 and eCount <=0):

        detail = "See the log file "+file +" for details"
        emailBody = "Error detected, Please see the log file "+file +" in "+Host +" for details"
        emailSubj = "Reconcile Error"
        sendEmail(emailTo, emailFrom, emailCC, emailBody, emailSubj)
        cCount = 0
        status = "ERROR"
    else:
        detail = "See the log file " +file + " for details"
        status = "ERROR"
        emailBody = "Please see the log file '"+file +" for error message in "+Host +" for details"
        emailSubj = "Reconcile error"
        sendEmail(emailTo, emailFrom, emailCC, emailBody, emailSubj)
        eCount = 0
    '''
    #logWrite(status, detail)
    print lines
    print "*****Reconcile complete, sent email if there was an error *****"
