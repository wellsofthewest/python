sjListOID = []
sjListURL = []

sjRows = arcpy.SearchCursor(addressSJ)
for row in sjRows:
    oid = row.getValue("OBJECTID")
    url = row.getValue("URL")
    sjListOID.append(oid)
    sjListURL.append(url)

l2Rows = arcpy.UpdateCursor(layer2)
for row in l2Rows:
    oid = row.getValue("OBJECTID")
    idx = sjListOID.index(oid)
    row.setValue("TLNO", sjListURL[idx])
    l2Rows.updateRow(row)