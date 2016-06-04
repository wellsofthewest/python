import arcpy, os

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


for machine in compList:
        arcpy.CreateEnterpriseGeodatabase_management("SQL_Server", '{0}'.format(machine), 'devsummit2016', "DATABASE_AUTH", 'sa', 'sa', "SDE_SCHEMA", 'sde', 'sde', '', r'C:\share\auth\Server_Ent_Adv.ecp')

