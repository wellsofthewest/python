#-------------------------------------------------------------------------------
# Name:           dbtune-python.py
# Purpose:        dbtune - SDE config CRUD.
#
# Author:         Ken G.
# Note:           Requires the pyodbc module - https://code.google.com/p/pyodbc/
# Created:        12/5/2014
# Version Tested: 9.3.1 - 10.3
#-------------------------------------------------------------------------------
import ctypes
import pyodbc

class Dbtune:
    def __init__(self, driver, server, database, user, password):
        """
        Construct the object with properties necessary to build a database connection string.  These properties 
        will automatically create the connection object used through the instance.
        
        Consult pyodbc documentation for connection string instructions and examples.
        https://code.google.com/p/pyodbc/
        
        Properties are:
        Driver:         i.e. "Sql Server" or "Oracle",
        Server:         Database server name.
        Database:       Database name.
        UID:            DB login user name.
        PWD:            DB Login password.
        """
        self.driver = driver
        self.server = server
        self.database = database
        self.user = user
        self.password = password
        self.conn = pyodbc.connect("DRIVER={" + driver + "}; SERVER=" + server + "; DATABASE=" + database + "; UID=" + user + "; PWD=" + password)

    def dbtuneCRUD(self, sql=[]):
        """
        This method requires an array containing the SQL operator such as UPDATE or INSERT and the desired values to modify.
        Depending on the operator specified, the necessary SQL statement is used.
        ("DEFAULTS", "B_CLUSTER_ROWID", "120")
        Example.
        myDbtune.dbtunCRUD(['SELECT','DEFAULTS','B_CLUSTER_ROWID','120'])
        >>>[(u'DEFAULTS', u'B_CLUSTER_ROWID', u'0')]
        
        TODO:
        
        How to overload a method in Python.  Each query needs a different set of values to run.  Different quantities in the passed array.
        For example, the select query does not need the configString value in the query.  The user doesn't know this which is why they 
        are querying the table in the first place.  Deleting an entry must be specific to each value for data safety.
        
        Example:
        To select:
        myDbtune.dbtunCRUD(['SELECT','DEFAULTS','B_CLUSTER_ROWID'])
        
        To delete
        myDbtune.dbtunCRUD(['DELETE','DEFAULTS','B_CLUSTER_ROWID','120'])
        """
        if len(sql) > 1:
            operator = sql[0]
            keyword = sql[1]
            parameterName = sql[2]
            configString = sql[3]
            if operator == "SELECT":
                try:
                    query = operator + " keyword, parameter_name, config_string FROM sde.sde_dbtune WHERE keyword = '{0}' AND parameter_name = '{1}'".format(keyword, parameterName, configString)
                    print self.queryDbtune(query)
                except Exception as err:
                    print err
                    
            if operator == "INSERT INTO":
                try:
                    query = str(operator) + " sde.sde_dbtune(keyword, parameter_name, config_string) VALUES ('{0}', '{1}', '{2}')".format(keyword, parameterName, configString)
                    self.queryDbtune(str(query))
                    print "Inserted keyword {0} with parameter {1} using {2} config string".format(keyword, parameterName, configString)
                except Exception as err:
                    print err
            
            if operator == "UPDATE":
                try:
                    query = str(operator) + " sde.sde_dbtune SET config_string = '{0}' WHERE keyword = '{1}' AND parameter_name = '{2}'".format(configString, keyword, parameterName)
                    self.queryDbtune(str(query))
                    print "Updated keyword {0} with parameter {1} using {2} config string".format(keyword, parameterName, configString)
                except Exception as err:
                    print err
            
            if operator == "DELETE":
                try:
                    query = str(operator) + " FROM sde.sde_dbtune WHERE keyword = '{0}' AND parameter_name = '{1}'".format(keyword, parameterName)
                    self.queryDbtune(str(query))
                    print "Deleted keyword {0} with parameter {1}".format(keyword, parameterName)
                except Exception as err:
                    print err
                    
    def queryDbtune(self, sql):
        try:
            cursor = self.conn.cursor() 
            result = cursor.execute(sql)
            #result.commit()
            return result.fetchall()
        except Exception as err:
            print err
    
    def confirmSQL(self, sql):
        try:
            confirm = self.dbtuneCRUD(["SELECT"])            
            for x in range(0, len(confirm)):
                print "DBTUNE updated:\t {0}->{1}->{2}".format(confirm[x][0],confirm[x][1],confirm[x][2])
        except Exception as err:
            print err
            
    def exportSQL(self, exportfile):
        try:
            cursor = self.conn.cursor()
            trunc = "TRUNCATE TABLE sde.sde_dbtune"
            print "Truncating DBTUNE table..."
            cursor.execute(str(trunc))
            cursor.commit()
            print "... DBTUNE truncated"
            print "Loading DBTUNE table with values from csv" #.format(str(exportfile))
            loadDbtune = "BULK INSERT sde.sde_dbtune FROM '" + exportfile + "' WITH (FIELDTERMINATOR = ';', ROWTERMINATOR = '\\n')"
            cursor.execute(str(loadDbtune))
            cursor.commit()
            print "DBTUNE successfully imported"
        except Exception as err:
            print err
    
    def DbtuneAlter(self, keyword, parameterName, value):
        try:
            self.dbtuneCRUD(["UPDATE", keyword, parameterName, value])
        except Exception as err:
            print err
    
    def DbtuneInsert(self, keyword, parameterName, value):
        try:
            self.dbtuneCRUD(["INSERT INTO", keyword, parameterName, value])
        except Exception as err:
            print err
            
    def DbtuneDelete(self, keyword, parameterName):
        try:
            self.dbtuneCRUD(["DELETE", keyword, parameterName, None ])
        except Exception as err:
            print err
               
    def DbtuneList(self, location):
        outfile = open(location, "w")
        dbtune = self.queryDbtune("SELECT * FROM sde.sde_dbtune")
        label = "<h4>DBTUNE Configuration for:</h4>"
        server = "<pre>%-12s %s" % ("\tServer:", str(self.server)) + "<br />"
        database = "%-12s %s" % ("\tDatabase:", str(self.database)) + "</pre><br />"
        dbtuneOutputHead = "<table border='1'><th>Keyword</th><th>Parameter Name</th><th>Config String</th>\n"
        outfile.write(label + server + database + dbtuneOutputHead)
        for i in range(0, len(dbtune)):
            dbtuneOutputBody = "<tr><td>" + dbtune[i][0] + "</td><td>" + dbtune[i][1] + "</td><td>" + dbtune[i][2] + "</td></tr>"
            outfile.write(dbtuneOutputBody)
        dbtuneOutputFoot = "</table>"
        outfile.write(dbtuneOutputFoot)
        try: 
            outfile.write(dbtuneOutputHead + dbtuneOutputBody + dbtuneOutputFoot)
            successMessage = "Operation Successful: Please see C:\\TEMP\\dbtune.html"
            print successMessage
        except Exception as err:
            return "Something went wrong: {0}".format(err)
    
    def DbtuneExport(self):
        try:
            outfile = open(r"C:\temp\dbtune.csv", "w")
            dbtune = self.queryDbtune("SELECT * FROM sde.sde_dbtune")
            for i in range(0, len(dbtune)):
                dbtuneOutputBody = dbtune[i][0] + ";" + dbtune[i][1] + ";" + dbtune[i][2] + "\n"
                outfile.write(dbtuneOutputBody)
            successMessage = "Operation Successful: Please see C:\\TEMP\\dbtune.csv"
            print successMessage
        except Exception as err:
            return "Something went wrong: {0}".format(err)
     
    def DbtuneImportSqlServer(self, exportfile=""):
        msg = ctypes.windll.user32.MessageBoxA(None, 'If a dbtune table exists, it will be truncated and replaced.  Would you like to continue?', 'Warning', 0x40 | 0x1)
        if msg == 6:
            try:
                self.exportSQL(exportfile)
            except Exception as err:
                print err
        else:
            print "Operation cancelled."
            

myDbtune = Dbtune("PostgreSQL OLE DB Provider", "KENFED21", "PGGDB", "sde", "sde")  
myDbtune.DbtuneList(r"D:\temp\dbtune.html")
#myDbtune.dbtuneCRUD(['SELECT','DEFAULTS','B_CLUSTER_ROWID','120'])
#myDbtune.DbtuneExport()  
#myDbtune.DbtuneDelete("DEFAULTS", "A_BIG_DEAL")       
#myDbtune.DbtuneAlter("DEFAULTS", "B_CLUSTER_ROWID", "120")
#myDbtune.DbtuneInsert("DEFAULTS", "A_BIG_DEAL", "0")   
#myDbtune.DbtuneImportSqlServer(r"C:\temp\dbtune.csv")