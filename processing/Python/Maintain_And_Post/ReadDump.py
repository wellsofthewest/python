import time, datetime, struct

inPath = r"C:\Incidents\Open\Kathryn\SJPW.dmp"
#inPath = r"C:\Incidents\Open\LEC\LEC-GIS-2015_08_24_163508.dmp"
#inPath = raw_input("DMP File: ")

inFile = open(inPath, 'r')
fileRead = inFile.read(600)

def dmpType (line):
    dpumpType = struct.unpack('B', line[477])[0]
    origType = struct.unpack('B', line[3])[0]
    if dpumpType == 49:
        return 'EXPDP'
        exit()
    if origType == 69:
        return 'EXP1'
        exit()
    if origType == 68:
        return 'EXP2'
        exit()

def dmpTime (line, dmpType):
    if dmpType == 'EXPDP':
        y,m,d,h,mm,s = struct.unpack('!HBBBBB', line[41:48])
        return datetime.datetime(y,m,d,h,mm,s)
    if dmpType == 'EXP1':
        date = struct.unpack('20c', line[108:128])
        x, M, d, T, y = ''.join(date).split(' ')
        h,mm,s = T.split(':')
        m = time.strptime(M, '%b').tm_mon
        return datetime.datetime(int(y),m,int(d),int(h),int(mm),int(s))
    if dmpType == 'EXP2':
        date = struct.unpack('20c', line[109:129])
        x, M, d, T, y = ''.join(date).split(' ')
        h,mm,s = T.split(':')
        m = time.strptime(M, '%b').tm_mon
        return datetime.datetime(int(y),m,int(d),int(h),int(mm),int(s))

def dmpVer (line, dmpType):
    if dmpType == 'EXPDP':
        ver = struct.unpack('14c', line[476:490])
        return ''.join(ver).replace('\x00', '')
    if dmpType == 'EXP1':
        ver = struct.unpack('8c', fileRead[11:19])
        return ''.join(ver)
    if dmpType == 'EXP2':
        ver = struct.unpack('8c', fileRead[13:21])
        return ''.join(ver)


    
dp = dmpType(fileRead)

print dmpTime(fileRead, dp)
print dmpVer(fileRead, dp)


#CLASSIC BLOCKSIZE
#print struct.unpack('4c', fileRead[35:39])


    
#EXPDP STATUS
dpumpType = struct.unpack('B', fileRead[477])[0]
origType = struct.unpack('B', fileRead[3])[0]

if dpumpType == 49:
    print "EXPDP"

    #BLOCKSIZE
    print struct.unpack('!H', fileRead[37:39])[0]

    #PLATFORM
    platform = struct.unpack('30c', fileRead[132:162])
    print(''.join(platform).replace('\x00', ''))

    #CHARACTER SET
    charset = struct.unpack('20c', fileRead[294:314])
    print(''.join(charset).replace('\x00', ''))

    #VERSION
    ver = struct.unpack('14c', fileRead[476:490])
    print(''.join(ver).replace('\x00', ''))

    #DATE
    y,m,d,h,mm,s = struct.unpack('!HBBBBB', fileRead[41:48])
    print "Dumpfile created on: {0}/{1}/{2} {3}:{4}:{5}".format(m,d,y,h,mm,s)

if origType == 69:
    print "EXP"

if origType == 68:
    print "EXP"

time.sleep(10)

