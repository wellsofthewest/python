import arcpy, subprocess

test = """C:\Python27\ArcGIS10.2\python.exe C:\Scripts\Python\SubPy.py"""
    

sqlProc = subprocess.Popen(test, stdout=subprocess.PIPE)
cmdReturn = sqlProc.communicate()[0]
print cmdReturn



