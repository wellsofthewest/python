import subprocess


users = []

domainGroups = ['net group "Supt-Desktop1" /domain',
'net group "Supt-Desktop2" /domain',
'net group "Supt-Desktop3" /domain',
'net group "Supt-Desktop4" /domain']


for domain in domainGroups:
    sqlProc = subprocess.Popen(domain, stdout=subprocess.PIPE)
    cmdReturn = sqlProc.communicate()[0]
    adminSplit = cmdReturn.split()
    for i in adminSplit[18:-4]:
        users.append(i)

addUser = """USE [master]
GO
CREATE LOGIN [AVWORLD\{0}] FROM WINDOWS WITH DEFAULT_DATABASE=[master]
GO
ALTER SERVER ROLE [sysadmin] ADD MEMBER [AVWORLD\{0}]
GO"""

for user in users:
    print addUser.format(user)

print len(users)


