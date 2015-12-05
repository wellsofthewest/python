import tempfile
import win32api
import win32print

filename = r"C:\Users\chri6962\Desktop\Rabbits\1.pdf"
win32api.ShellExecute (0,"print",filename,'/d:"%s"' % win32print.GetDefaultPrinter (),".",0)
