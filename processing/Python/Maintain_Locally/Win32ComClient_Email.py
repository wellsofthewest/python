#Import OS and Win32Com Client modules
import os, win32com.client

#Open/Call Outlook
outlook = win32com.client.Dispatch("Outlook.Application")

#Create new email message
email = outlook.CreateItem(0)

#Populate Subject Line
email.Subject = "Manual"

#Populate Body
email.Body = "Here you go"

#Populate Email recipients
email.To = "christian_wells@esri.com"

#Add Attachments
email.Attachments.Add(finalpdf_filename)

#Send email
email.send

#Import Win32API and Print
import win32api
import win32print

#Print file
win32api.ShellExecute (0,"print",finalpdf_filename,'/d:"%s"' % win32print.GetDefaultPrinter (),".",0)


