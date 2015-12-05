import arcpy, os

# Create an output directory variable
#
outDir = r"C:\temp\MBExample\final_output"  

# Create a new, empty pdf document in the specified output directory
#
finalpdf_filename = outDir + r"\FinalMB.pdf"
if os.path.exists(finalpdf_filename):
  os.remove(finalpdf_filename)
finalPdf = arcpy.mapping.PDFDocumentCreate(finalpdf_filename)

# Add the title page to the pdf
#
finalPdf.appendPages(r"C:\temp\MBExample\ancillary_pages\TitlePage.pdf")

# Add the index map to the pdf
#
finalPdf.appendPages(r"C:\temp\MBExample\maps\IndexMap.pdf")

# Create Facing Pages for the map book
# Create pages for left-hand side of the book
#
mxdPathLeft = r"C:\temp\MBExample\maps\Arenac County MB Left.mxd"
tempMapLeft = arcpy.mapping.MapDocument(mxdPathLeft)
tempDDPLeft = tempMapLeft.dataDrivenPages

# Loop creates individual pdf's for odd numbered pages
#
for pgNumLeft in range(1, tempDDPLeft.pageCount + 1, 2):
  temp_filename = r"C:\temp\MBExample\temp_pdfs\MB_" + \
                            str(pgNumLeft) + ".pdf"
  if os.path.exists(temp_filename):
    os.remove(temp_filename)
  tempDDPLeft.exportToPDF(temp_filename, "RANGE", pgNumLeft)

# Create pages for right-hand side of the book
#
mxdPathRight = r"C:\temp\MBExample\maps\Arenac County MB Right.mxd"
tempMapRight = arcpy.mapping.MapDocument(mxdPathRight)
tempDDPRight = tempMapRight.dataDrivenPages

# Loop creates individual pdf's for even numbered pages
#
for pgNumRight in range(2, tempDDPRight.pageCount + 1, 2):
  temp_filename = r"C:\temp\MBExample\temp_pdfs\MB_" + \
                             str(pgNumRight) + ".pdf"
  if os.path.exists(temp_filename):
    os.remove(temp_filename)
  tempDDPRight.exportToPDF(temp_filename, "RANGE", pgNumRight)

# Append right and left-hand pages together in proper order
#
for pgNum in range(1, tempDDPLeft.pageCount + 1):
  print "Page", pgNum, "of", tempDDPLeft.pageCount
  tempPDF = r"C:\temp\MBExample\temp_pdfs\MB_" + str(pgNum) + ".pdf"
  finalPdf.appendPages(tempPDF)

# Update the properties of the final pdf
#
finalPdf.updateDocProperties(pdf_open_view="USE_THUMBS",
                             pdf_layout="SINGLE_PAGE")

# Save your result
#
finalPdf.saveAndClose()

# Delete variables
#
del finalPdf, mxdPathLeft, mxdPathRight, tempDDPLeft, tempDDPRight, 
tempMapLeft, tempMapRight, tempPDF
