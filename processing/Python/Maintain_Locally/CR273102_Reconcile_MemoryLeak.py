#-------------------------------------------------------------------------------
# Name:         CR273102_Reconcile_MemoryLeak.py
# Purpose:      To monitor memory comsumption while reconciling 5 versions.
#
# Author:       Shawn Thorne
#               ESRI Inc.
#
# Created:      10.4.2013
# Updated:      10.5.2013
#
# References:   http://windows.microsoft.com/en-US/windows7/What-is-virtual-memory
#               http://resources.arcgis.com/en/help/main/10.2/index.html#//00170000015p000000
#
#-------------------------------------------------------------------------------

import arcpy
import wmi
import time
import gc


mem = wmi.WMI()
process = 'python.exe'


def main():
    try:
##
##        beginVMem= mem.Win32_Process(Name = process)
##        BeginVMem = beginVMem[0].VirtualSize
##        print ("\n Beginning Virtual Size Memory     : {}".format(str(int(BeginVMem)/1024)))

        beginWsMem = mem.Win32_Process(Name = process)
        BeginWSMem = beginWsMem[0].WorkingSetSize
        print (" Beginning Working Set Size Memory : {}\n".format(str(int(BeginWSMem)/1024)))

        EGDB = arcpy.env.workspace = r'Database Connections\PEPCO1 - SDE@ZIP1.sde'
        #EGDB = arcpy.env.workspace = r'Database Connections\malibu.sde'

        if not arcpy.Exists(EGDB):
            print("\n The specified SDE Connection File DOES NOT EXIST!!\n")
            return

        else:

            print("\n The specified SDE Connection File EXISTS!!\n\n")

            editVersion = None
            targetVersion = "SDE.DEFAULT"

            cnt = 0
            RecStartTime = 0
            RecStopTime = 0
            TotalRecTime = 0

            versionList = ['GIStoEMS','WR3354808_REV12956','WR3359423_REV9183','WR3365142_REV15855','WR3378067_REV37284']

            for editVersion in versionList:

##                vmemBefore = mem.Win32_Process(Name = process)
##                VMemBefore = vmemBefore[0].VirtualSize
##                print (" Virtual Size Memory used by '{}' process BEFORE Reconcile (in KBs)     : {}".format(process,str(int(VMemBefore)/1024)))

                wsmemBefore = mem.Win32_Process(Name = process)
                WSMemBefore = wsmemBefore[0].WorkingSetSize
                print (" Working Set Size Memory used by '{}' process BEFORE Reconcile (in KBs) : {}".format(process,str(int(WSMemBefore)/1024)))

                print("   Reconciling Version '{}' with '{}'".format(editVersion,targetVersion))

                RecStartTime = time.time()

                rec = arcpy.management.ReconcileVersions(EGDB, 'ALL_VERSIONS', targetVersion, editVersion, 'NO_LOCK_ACQUIRED', 'NO_ABORT', 'BY_OBJECT', 'FAVOR_TARGET_VERSION', 'NO_POST', 'KEEP_VERSION', '')

                RecStopTime = time.time() - RecStartTime

                print("   Successfully Reconciled Version '{}' with '{}' - Elapsed time (in secs) : {}".format(editVersion,targetVersion,str(round(RecStopTime,2))))

                TotalRecTime = TotalRecTime + RecStopTime
                RecStartTime = 0
                RecStopTime = 0
                editVersion = None
                cnt += 1

##                vmemAfter = mem.Win32_Process(Name = process)
##                VMemAfter = vmemAfter[0].VirtualSize
##                print (" Virtual Size Memory used by '{}' process AFTER Reconcile (in KBs)      : {}".format(process,str(int(VMemAfter)/1024)))

                wsmemAfter = mem.Win32_Process(Name = process)
                WSMemAfter = wsmemAfter[0].WorkingSetSize
                print (" Working Set Size Memory used by '{}' process AFTER Reconcile (in KBs)  : {}\n\n".format(process,str(int(WSMemAfter)/1024)))


        print("\n\n Total # of Versions Reconciled : {}".format(str(cnt)))
        print(" Total Reconcile Time (in secs) : {}\n".format(str(round(TotalRecTime,2))))

        print("\n\n COMPLETED!!\n")

        gc.collect()

##        endVMem = mem.Win32_Process(Name = process)
##        EndVMem = endVMem[0].VirtualSize
##        print ("\n Ending Virtual Size Memory      : {}".format(str(int(EndVMem)/1024)))

        endWsMem = mem.Win32_Process(Name = process)
        EndWSMem = endWsMem[0].WorkingSetSize
        print (" Ending Working Set Size Memory  : {}\n\n".format(str(int(EndWSMem)/1024)))


    except arcpy.ExecuteError:
        print (arcpy.GetMessages(2))

    except Exception as e:
        print (e[0])

if __name__ == '__main__':
    main()





