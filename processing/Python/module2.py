import arcpy, os, numpy

path = r"C:\Users\chri6962\Verify_GN"
fc = r"c:\users\chri6962\Verify_GN\extFGDB.gdb\extGrids"

sizes = []
grids = {}

for f in os.listdir(path):
    sizes.append(os.path.getsize(os.path.join(path, f)))
    grids.update({'{}'.format(os.path.splitext(f[12:])[0]):os.path.getsize(os.path.join(path, f))})


arr = numpy.array(sizes)
mean = numpy.mean(arr)
std =  numpy.std(arr)

cur = arcpy.da.UpdateCursor(fc, ['OID@', 'Z_SCORE', 'MEAN', 'STD'])

for row in cur:
    row[1] = (grids[str(row[0])] - mean)/std
    row[2] = mean
    row[3] = std
    cur.updateRow(row)


