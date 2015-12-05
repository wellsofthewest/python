import arcpy, os

nFields = raw_input('How many fields do you want to add?:')

gdb = r'c:\share\Nana.gdb'

fc = 'Nana'

for i in range(1, int(nFields)+1):
    arcpy.AddField_management(os.path.join(gdb, fc), 'F{}'.format(i), 'TEXT')

