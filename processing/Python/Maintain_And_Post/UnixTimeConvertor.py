import arcpy, os, datetime, time

uxTime = raw_input("Enter the Unix Epoch time here: ")

dTime = time.strftime('%d-%b-%Y %H:%M:%S', time.localtime(int(1431716487)))

print dTime

time.sleep(4)
