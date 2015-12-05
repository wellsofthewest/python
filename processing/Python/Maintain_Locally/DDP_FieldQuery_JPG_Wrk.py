#DDP: Set Definition Query on a secondary Grid
#Import Modules
import arcpy, os

arcpy.env.workspace = r"C:\Users\chri6962\Documents\ArcGIS\Packages\DDP_Index2\v101\datadrivenpages.gdb"

# Set Variables
mxdpath = r'C:\Users\chri6962\Documents\ArcGIS\Packages\DDP_Index2\v101\DDP_Index2.mxd' # string
outputfolder = 'C:\JPEG' # string
namefield = 'Index1'
#value = ''
queryfield = 'Index2' # string
#layers = ['DefQry2=Grid2'] # list
lyrName = ''
cnt1 = 0
cnt2 = 0
cnt3 = 0
mxd = arcpy.mapping.MapDocument(mxdpath)

#Reference data frames
df = arcpy.mapping.ListDataFrames(mxd, "")[1]
'''

for pageNum in range(1, mxd.dataDrivenPages.pageCount + 1):
    mxd.dataDrivenPages.currentPageID = pageNum # set the current page
    pageName = mxd.dataDrivenPages.pageRow.getValue(namefield) # get the pageName
    pageName += '.jpg' # add '.pdf' extension for file name
    jpeg = os.path.join(outputfolder, pageName) # add pageName to output folder to get full output path
    # Start Loop through all layers of mxd file

    for lyr in arcpy.mapping.ListLayers(mxd): # for every layer in mxd's Layer List
        lyrName = lyr.name
        value = mxd.dataDrivenPages.pageRow.getValue(queryfield)
        print value
        if lyrName == 'DefQry2Grid2':   #in layers: # if layer name in user input list above
            query = queryfield + "=" + "\"" + value + "\"" # else create a new query
            lyr.definitionQuery = query # set the layers defintionQuery
            cnt2 = cnt2 + 1
            print cnt2
            print lyr.name
            print query

        elif lyrName == 'DefQry2NOTGrid2':   #in layers: # if layer name in user input list above
            query = queryfield + "<>" + "\"" + value + "\"" # else create a new query
            lyr.definitionQuery = query # set the layers defintionQuery
            cnt2 = cnt2 + 1
            print cnt2
            print lyr.name
            print query
        else:
            print 'Next' # else print next, this isn't necassary, but its a good place holder
'''

Index2Value = mxd.dataDrivenPages.pageRow.getValue('Index2')
query = "\"Index2\"='Indiana'"
print query
lyr2 = arcpy.mapping.ListLayers(mxd, "DefQry2Grid2", df)[0]
y =arcpy.SelectLayerByAttribute_management(lyr2, "NEW_SELECTION", query).getOutput(0)
x = y.getSelectedExtent(True)
print (type(y))
df.extent = arcpy.Extent(y.XMin, y.YMin, y.XMax, y.YMax)

'''
    #arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION")

    #Print some helps & then export file
    print pageName
    cnt1 = 0
    cnt2 = 0
    cnt3 = cnt3 + 1
    arcpy.mapping.ExportToJPEG(mxd, jpeg) # export the current Page to pdf
print cnt3
del mxd, lyr, pageName, pageNum, query, value
'''