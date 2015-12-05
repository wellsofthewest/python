import sys
import arcpy


# POINTS TO MY VERSION OF STAGING:
WORKSPACE = r"C:\Users\chri6962\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\Connection to cwells.sde"
arcpy.env.workspace = WORKSPACE

print "********************** Concatenating parcels easement, opp, row **********************"
parcels = "c1022.SDE.PARCELS_TEST"
fields = ("ESMT_NUM_0", "ESMT_NUM_1", "ESMT_NUM_2", "ESMT_NUM_3", "ESMT_NUM_4", "ESMT_NUM_5", "ESMT_NUM_6", "ESMT_NUM_7",
"ESMT_NUM_ALL","OP_NUM", "OP_NUM_1", "OP_NUM_2", "OP_NUM_3", "OpNumOall","ROW_NUM", "ROW_NUM_1", "ROW_NUM_2", "ROWNumOaLL", "OID@")
count = 0
count2 = 0
try:
    edit = arcpy.da.Editor(WORKSPACE)
    edit.startEditing(False, True)
    edit.startOperation()
    with arcpy.da.UpdateCursor(parcels, fields) as updateCur:
        for row in updateCur:
            count2 += 1
            updateCur.updateRow(row)
    edit.stopOperation()
    edit.stopEditing(True)

except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
    print "Parcels fail!  Execute Error"
except Exception as e:
    tb = sys.exc_info()[2]
    print "Line " + str(tb.tb_lineno)
    print "Error " + str(e.args[0])
    print "Parcels fail!"
finally:
    print "********************** finished parcels easement, op, row. **********************"
    print str(count) + " parcel rows updated."
    print str(count2) + " count2."
