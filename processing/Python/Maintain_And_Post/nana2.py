import os, datetime, time, sched, shutil

timestamp = int(time.time())

path = r"C:\Share\Nana.gdb"
tmp = r"C:\temp"

scheduler = sched.scheduler(time.time, time.sleep)

def fileCopy(name):
    timestamp = int(time.time())
    newDir = os.path.join(tmp, 'Locks_{}'.format(timestamp))
    os.mkdir(newDir)
    for f in os.listdir(path):
        basename, extension = os.path.splitext(os.path.join(path, f))
        if extension.lower() == '.lock':
            filePath = path
            destPath = os.path.join(tmp, newDir)
            xc = 'robocopy {} {} {}'.format(filePath, destPath, f)
            os.system(xc)
    scheduler.enter(1, 1, fileCopy, ('test',))


scheduler.enter(0, 1, fileCopy, ('test',))
scheduler.run()

















