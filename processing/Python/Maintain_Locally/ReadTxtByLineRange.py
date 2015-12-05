#Path of the file you want to read
inPath = r"C:\Incidents\Open\pge\pge.dmp"

#Path of the file to be written
##outPath = r"C:\Incidents\Open\01596063_DataPump\test.txt"

inFile = open(inPath, 'rb')
##outFile = open(outPath, 'w')

##lines = inFile.readlines()[1646607]

#Specify the range of values to be read ***NOTE: Increase the upper line number by one value
##for i in range(0, 500):
##    outFile.write(lines[i])
##
##with open(inPath, 'rb') as f:
##    print sum(1 for _ in f)

for line in inFile:
    print line

##cnt = 0
##
##try:
##    for line in inFile:
##        cnt += 1
##except:
##    print cnt

#Close Text File
##inFile.close()
##outFile.close()


##def _make_gen(reader):
##    b = reader(1024 * 1024)
##    while b:
##        yield b
##        b = reader(1024*1024)
##
##def rawpycount(filename):
##    f = open(filename, 'rb')
##    f_gen = _make_gen(f.read)
##    return sum( buf.count(b'\n') for buf in f_gen )
##
##test = rawpycount(inPath)

