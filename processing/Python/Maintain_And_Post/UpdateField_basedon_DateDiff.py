import arcpy, datetime

table = r"C:\Users\chri6962\Desktop\BackflowDatabase\BackflowDatabase\BackflowTest.gdb\Backflow\Backflow"
field = "Pass_Fail"
codeblock = """def timeDif(date2, status):
    date1 = datetime.date.today()
    date2str = str(date2)
    month, date, year = date2.split('/')
    featDate2 = datetime.date(int(year), int(month), int(date))
    timediff = date1 - featDate2
    if timediff>=datetime.timedelta(days=365):
        return "Expired"
    else:
        return status"""

expression = "timeDif( !Insp_Date!, !Pass_Fail! )"

arcpy.CalculateField_management(table, field, expression, "PYTHON_9.3", codeblock)
