import subprocess


users = []

domainGroups = ['net group "Supt-GDT-Redlands1" /domain', 'net group "Supt-GDT-Redlands2" /domain']


for domain in domainGroups:
    sqlProc = subprocess.Popen(domain, stdout=subprocess.PIPE)
    cmdReturn = sqlProc.communicate()[0]
    adminSplit = cmdReturn.split()
    for i in adminSplit[18:-4]:
        users.append(i)

for user in users:
    print user


