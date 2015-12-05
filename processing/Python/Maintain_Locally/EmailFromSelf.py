import arcpy, os, win32com.client

finalpdf_filename = r"C:\Users\chri6962\Desktop\PythonAThon\AlexEmail.py"

arcpy.AddMessage("Preparing Email")
outlook = win32com.client.Dispatch("Outlook.Application")
email = outlook.CreateItem(0)
email.Subject = "Manual"
email.Body = "Here you go"
email.To = "anohe@esri.com"
email.Attachments.Add(finalpdf_filename)
email.send

import win32api
import win32print



win32api.ShellExecute (0,"print",finalpdf_filename,'/d:"%s"' % win32print.GetDefaultPrinter (),".",0)


