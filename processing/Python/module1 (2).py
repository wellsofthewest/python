import arcpy, os

path = r"C:\Users\chri6962\Verify_GN"


def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

for i in os.listdir(path):
    print '{0:50}: {1:20}'.format(i, get_size(os.path.join(path, i)))