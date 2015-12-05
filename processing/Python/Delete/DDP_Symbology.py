import arcpy, os

mxdFile = r"C:\Users\chri6962\Desktop\Untitled2.mxd"
mxd = arcpy.mapping.MapDocument(mxdFile)
lyr = arcpy.mapping.ListLayers(mxd)[0]

valueList = [u'Cabernet Franc', u'Petite Verdot', u'Sauvignon Blanc', u'Petit Sirah', u'Cabernet Sauvignon', u'Petite Syrah', u'Cabernet franc', u'Cabernet sauvignon', u'Carmenere', u'Chardonnay', u'Grenache', u'Malbec', u'Merlot', u'Nebiolo', u'Muscat Blanc', u'Petit Syrah', u'Petit Verdot', u'Pinot Noir', u'Primitivo', u'Sangiovese', u'Sauvignon blanc', u'Sauvignon Musque', u'Semillon', u'St. Macaire', u'Syrah', u'Shiraz', u'Viognier', u'Voignier', u'Zinfandel']
valueDict = {'Cabernet Franc':0,
'Petite Verdot':1,
'Sauvignon Blanc':2,
'Petit Sirah':3,
'Cabernet Sauvignon':4,
'Petite Syrah':5,
'Cabernet franc':6,
'Cabernet sauvignon':7,
'Carmenere':8,
'Chardonnay':9,
'Grenache':10,
'Malbec':11,
'Merlot':12,
'Nebiolo':13,
'Muscat Blanc':14,
'Petit Syrah':15,
'Petit Verdot':16,
'Pinot Noir':17,
'Primitivo':18,
'Sangiovese':19,
'Sauvignon blanc':20,
'Sauvignon Musque':21,
'Semillon':22,
'St. Macaire':23,
'Syrah':24,
'Shiraz':25,
'Viognier':26,
'Voignier':27,
'Zinfandel':28}


for pageNum in range(1, mxd.dataDrivenPages.pageCount + 1):
    mxd.dataDrivenPages.currentPageID = pageNum
    value = mxd.dataDrivenPages.pageRow.getValue("Ranch")
    rows = arcpy.da.SearchCursor(lyr, ['Sum_Acres', 'Variety'], "Ranch = '{0}'".format(value))
    print pageNum
    print "\t",value
    for row in rows:
        variety = row[1]
        acres = row[0]
        valueList[valueDict[variety]] = "{0}: {1}".format(variety, acres)
    print valueList
    lyr.symbology.classLabels = valueList
    arcpy.mapping.ExportToPDF(mxd, r"C:\temp\{0}.pdf".format(value))



