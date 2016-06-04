""" Code to repair file geodatabases where the compression (or uncompression) halted
because the gdbtable was locked."""

### From the command prompt, place the corrupted File GDB and this python script in the same directory (eg: C:\zTemp)
### Navigate to the directory from command line and run the script using the following arguments.
### For example,
### C:\zTemp>C:\Python27\ArcGIS10.3\python.exe RepairCompressFailure.py CorruptedFileGDB.gdb
### Run from Windows Command Prompt


import glob, os, sys, time

gdb = raw_input("Corrupted File Geodatabase Path: ")

### Verify that the file geodatabase exists.
if not (os.path.isdir(gdb)):
	print gdb + " does not exist."
	exit(0)

### Make a list of files with a tmp extension.
path = gdb
os.chdir(path)
files = glob.glob("*.tmp")

### Delete the existing .gdbtable files.
for file in files:
	os.remove(file.replace(".tmp",".gdbtable"))


### Rename the .tmp files to .gdbtable files.
for file in files:
	os.rename(file, file.replace(".tmp",".gdbtable"))


###Successful completion of script
print "Script completed"
time.sleep(5)