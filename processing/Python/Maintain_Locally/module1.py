import arcpy, subprocess, pyodbc, cx_Oracle, datetime, getpass

instance = raw_input("Oracle Instance: ")
username = raw_input("SDE Username: ")
password = getpass.getpass("SDE Password: ")

print instance, username, password