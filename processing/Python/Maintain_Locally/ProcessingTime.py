import time
from time import localtime, strftime

startTime = strftime("%H%M%S", localtime())
arcpy.AddMessage("Starting Range Process at: " + strftime("%H:%M:%S", localtime()))

#Process goes here

endTime=strftime("%H%M%S", localtime())
arcpy.AddMessage("Ending Range Process: " + strftime("%H:%M:%S", localtime()))
totalTime = (int(endTime) - int(startTime))
arcpy.AddMessage("Total Process Time in Seconds: " + str(totalTime))
