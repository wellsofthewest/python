import os, subprocess, arcpy

#Set connection parameters
gdb = r"Database Connections\Geneva.sde"
conn = arcpy.ArcSDESQLExecute("cwells", "sde:oracle11g:cwells/geneva", "", "sys", "sys")
sdeFC = r"Database Connections\Geneva.sde\SDE.FEMA"
gdbFC = r"C:\Incidents\Closed\1186238_IntersectToolCrash\femapnls.shp"
traceName = "APPEND"

#Flush buffer cache and shared pool
conn.execute("ALTER SYSTEM FLUSH BUFFER_CACHE")
conn.execute("ALTER SYSTEM FLUSH SHARED_POOL")

#Set Tracefile Identifier
conn.execute("alter session set tracefile_identifier = '{0}'".format(traceName))

#Begin Trace
conn.execute("alter system set events '10046 trace name context forever,level 12'")

#Perform workflow
arcpy.Append_management(gdbFC, sdeFC, "NO_TEST")

#End Trace
conn.execute("alter system set events '10046 trace name context off'")

#Convert Trace through TKPROF
trace_dest = r"D:\app\chri6962\diag\rdbms\geneva\geneva\trace"
for trace in os.listdir(trace_dest):
    if traceName in trace and "trc" in trace:
        trc = os.path.join(trace_dest, trace)
        trcName,ext = trace.split(".")
        tkprof = os.path.join(trace_dest, trcName + ".txt")
        subprocess.call(["tkprof", trc, tkprof, "EXPLAIN=sde/sde@cwells/geneva", "SYS=YES", "TABLE=SDE.EXPLAIN_PLAN"])






