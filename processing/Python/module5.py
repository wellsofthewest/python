import arcpy, os, subprocess

compList = ['0132TECHSUPP',
'0133TECHSUPP',
'0134TECHSUPP',
'0135TECHSUPP',
'0136TECHSUPP',
'0137TECHSUPP',
'0138TECHSUPP',
'0139TECHSUPP',
'0140TECHSUPP',
'0141TECHSUPP',
'0142TECHSUPP',
'0143TECHSUPP',
'0144TECHSUPP',
'0145TECHSUPP',
'0146TECHSUPP',
'0147TECHSUPP',
'0148TECHSUPP',
'0149TECHSUPP',
'0150TECHSUPP']

cmd = """
Import-Module "sqlps"

$smo = 'Microsoft.SqlServer.Management.Smo.'
$wmi = new-object ($smo + 'Wmi.ManagedComputer')

# List the object properties, including the instance names.
$Wmi

# Enable the TCP protocol on the default instance.
$uri = "ManagedComputer[@Name='{0}']/ ServerInstance[@Name='MSSQLSERVER']/ServerProtocol[@Name='Tcp']"
$Tcp = $wmi.GetSmoObject($uri)
$Tcp.IsEnabled = $false
$Tcp.Alter()
$Tcp

# Enable the named pipes protocol for the default instance.
$uri = "ManagedComputer[@Name='{0}']/ ServerInstance[@Name='MSSQLSERVER']/ServerProtocol[@Name='Np']"
$Np = $wmi.GetSmoObject($uri)
$Np.IsEnabled = $true
$Np.Alter()
$Np

# Get a reference to the ManagedComputer class.
CD SQLSERVER:\SQL\{0}
$Wmi = (get-item .).ManagedComputer
# Get a reference to the default instance of the Database Engine.
$DfltInstance = $Wmi.Services['MSSQLSERVER']
# Display the state of the service.
$DfltInstance
# Stop the service.
$DfltInstance.Stop();
# Wait until the service has time to stop.
# Refresh the cache.
$DfltInstance.Refresh();
# Display the state of the service.
$DfltInstance
# Start the service again.
$DfltInstance.Start();
# Wait until the service has time to start.
# Refresh the cache and display the state of the service.
$DfltInstance.Refresh();
$DfltInstance

$Exit
"""

outdir = os.path.expanduser('~')
fldName = 'cmds'

if not os.path.exists(os.path.join(outdir, fldName)):
    os.mkdir(os.path.join(outdir, fldName))

for machine in compList:
    outfile = os.path.join(r"\\cwells\share", machine + '.py')
    py = """arcpy.CreateDatabaseConnection_management('Database Connections', 'sde@devsummit2016', "SQL_SERVER", '{0}', "DATABASE_AUTH", 'SDE', 'sde')"""
    f = open(outfile, "wb+")
    f.write("import arcpy, os\n")
    f.write(py.format(machine))
    f.close()
    #print "Invoke-Command -ComputerName {0} -ScriptBlock {{copy \\cwells\share\{0}.py C:\users\demo\{0}.py}} -credential $demo".format(machine)
    #sblk = """C:\Python27\ArcGIS10.3\python.exe C:\users\demo\{0}.py""".format(machine)
    #print "Invoke-Command -ComputerName {0} -ScriptBlock {{{1}}} -credential $demo".format(machine, sblk)
##    print "Invoke-Command -ComputerName {0} -FilePath C:\Users\chri6962\cmds\{0}.ps1 -credential uc\demo".format(machine)