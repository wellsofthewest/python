def gatherDB():
    import os, arcpy, shutil, time, datetime
    arcpy.env.overwriteOutput = True

    print 'This utility is going to prompt you for database connection information \nto see if Python is able to connect to the database through a variety \nof methods.\n\nThis tool is designed for use with SQL Server only.\n'

    userHome = os.path.expanduser("~")
    workPath = os.path.join(userHome, "SDETest")

    if os.path.exists(workPath) == False:
        os.mkdir(workPath)

    outLog = open(os.path.join(workPath, "LogFile.txt"), "w+")

    serverName = raw_input("Server Name: ")
    instanceName = raw_input("Instance Name: ")
    username = raw_input("Username: ")
    password = raw_input("Password: ")
    databaseName = raw_input("Database: ")
    sdeName = "esritest.sde"

    print "\nPlease wait while we attempt to connect to the database"

    outLog.write('Attempting to connect to the database via ODBC and ArcSDESQLExecute\n\tInstance: {0}\n\tDatabase: {1}\n\tUser: {2}'.format(serverName,
                                                                                                                                             databaseName,
                                                                                                                                             username))

    try:
        conn = arcpy.ArcSDESQLExecute(serverName, "sde:sqlserver:{0}".format(instanceName), databaseName, username, password)

        if conn.execute('select description from sde.sde_version') <> False:
            outLog.write('\n\n\tPython was able to make a direct connection to the database using ODBC drivers')
            outLog.write("\n\t\tThis GDB version is: " + conn.execute('select description from sde.sde_version'))

    except:
        outLog.write('\n\tPython was NOT able to make a direct connection to the database using ODBC drivers')

    outLog.write('\n\nAttempting to create an SDE Connection file to the geodatabase')
    try:
        arcpy.CreateDatabaseConnection_management(out_folder_path=workPath,
                                                  out_name=sdeName,
                                                  database_platform='SQL_SERVER',
                                                  instance=instanceName,
                                                  account_authentication='DATABASE_AUTH',
                                                  username=username,
                                                  password=password,
                                                  database=databaseName)
        outLog.write('\n\tSDE Connection File Created')
    except:
        outLog.write('\n\tSDE Connection File Creation Failed')

    outLog.write('\n\nAttempting to list the connected users from SDE File')
    try:
        print datetime.datetime.now()
        users = arcpy.ListUsers(os.path.join(workPath, sdeName))
        for user in users:
            outLog.write('\n\tUser Connected: {0}'.format(user.Name))
        outLog.write('\n\tUsers are able to be listed')
        print datetime.datetime.now()
    except:
        outLog.write('\n\tUsers are NOT able to be listed')


    print "\nPlease delete the following directory upon resolution:\n{0}".format(workPath)
    time.sleep(10)
    os.startfile(os.path.join(workPath, "LogFile.txt"))

if __name__ == '__main__':
    gatherDB()
