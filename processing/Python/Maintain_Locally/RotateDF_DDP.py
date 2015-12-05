import os
import arcpy


#Create an output directory variable

outDir = r"C:\Users\chri0000\Desktop\DDExportTest"  

# Create a new, empty pdf document in the specified output directory
#
finalpdf_filename = outDir + r"\FinalMB.pdf"
if os.path.exists(finalpdf_filename):
  os.remove(finalpdf_filename)
finalPdf = arcpy.mapping.PDFDocumentCreate(finalpdf_filename)

# Add the title page to the pdf
#
finalPdf.appendPages(outDir + os.sep + "TitlePage.pdf")

# Add the index map to the pdf
#
finalPdf.appendPages(outDir + os.sep + "IndexMap.pdf")


# Create Facing Pages for the map book
# Create pages for left-hand side of the book
#
mxdPathLeft = r"C:\Users\chri0000\Desktop\DDExportTest\Left.mxd" 
tempMapLeft = arcpy.mapping.MapDocument(mxdPathLeft)
tempDDPLeft = tempMapLeft.dataDrivenPages

# Loop creates individual pdf's for odd numbered pages
#
for pgNumLeft in range(1, tempDDPLeft.pageCount + 1, 2):
  temp_filename = outDir + os.sep + str(pgNumLeft) + ".pdf"
  if os.path.exists(temp_filename):
    os.remove(temp_filename)
  tempDDPLeft.exportToPDF(temp_filename, "RANGE", pgNumLeft)

# Create pages for right-hand side of the book
#
mxdPathRight = r"C:\Users\chri0000\Desktop\DDExportTest\Right.mxd" 
tempMapRight = arcpy.mapping.MapDocument(mxdPathRight)
tempDDPRight = tempMapRight.dataDrivenPages

# Loop creates individual pdf's for even numbered pages
#
for pgNumRight in range(2, tempDDPRight.pageCount + 1, 2):
  temp_filename = outDir + os.sep + str(pgNumRight) + ".pdf"
  if os.path.exists(temp_filename):
    os.remove(temp_filename)
  for df in arcpy.mapping.ListDataFrames(mxdPathRight, "N*"):
    df.rotation = 15
  tempDDPRight.exportToPDF(temp_filename, "RANGE", pgNumRight)


# Append right and left-hand pages together in proper order
#
for pgNum in range(1, tempDDPLeft.pageCount + 1):
  print "Page", pgNum, "of", tempDDPLeft.pageCount
  tempPDF = r"C:\Users\chri0000\Desktop\DDExportTest" + os.sep + str(pgNum) + ".pdf"
  finalPdf.appendPages(tempPDF)

# Update the properties of the final pdf
#
finalPdf.updateDocProperties(pdf_open_view="USE_THUMBS", pdf_layout="SINGLE_PAGE")

# Save your result
#
finalPdf.saveAndClose()

# Delete variables
#
del finalPdf, mxdPathLeft, mxdPathRight, tempDDPLeft, tempDDPRight, 
tempMapLeft, tempMapRight, tempPDF

