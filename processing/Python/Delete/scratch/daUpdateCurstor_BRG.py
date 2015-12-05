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
            ease_all = ""
            op_all = ""
            row_all = ""
            count2 += 1
            update = False
            if row[0] is not None and row[0] != "":
                ease_all += row[0] + ", "
            if row[1] is not None and row[1] != "":
                ease_all += row[1] + ", "
            if row[2] is not None and row[2] != "":
                ease_all += row[2] + ", "
            if row[3] is not None and row[3] != "":
                ease_all += row[3] + ", "
            if row[4] is not None and row[4] != "":
                ease_all += row[4] + ", "
            if row[5] is not None and row[5] != "":
                ease_all += row[5] + ", "
            if row[6] is not None and row[6] != "":
                ease_all += row[6] + ", "
            if row[7] is not None and row[7] != "":
                ease_all += row[7] + ", "
            if ease_all != "":
                ease_all = ease_all.strip().rstrip(", ")
                update = True
                ##print "ESMT setting OID: " + str(row[18]) + " from " + str(row[8]) + " to " + ease_all
                row[8] = ease_all
            if row[9] is not None and row[9] != "":
                op_all += row[9] + ", "
            if row[10] is not None and row[10] != "":
                op_all += row[10] + ", "
            if row[11] is not None and row[11] != "":
                op_all += row[11] + ", "
            if row[12] is not None and row[12] != "":
                op_all += row[12] + ", "
            if op_all != "":
                op_all = op_all.strip().rstrip(", ")
                update = True
                ##print "OP setting OID: " + str(row[18]) + " from " + str(row[13]) + " to " + op_all
                row[13] = op_all
            if row[14] is not None and row[14] != "":
                row_all += row[14] + ", "
            if row[15] is not None and row[15] != "":
                row_all += row[15] + ", "
            if row[16] is not None and row[16] != "":
                row_all += row[16] + ", "
            if row_all != "":
                row_all = row_all.strip().rstrip(", ")
                update = True
                ##print "ROW setting OID: " + str(row[18]) + " from " + str(row[17]) + " to " + row_all
                row[17] = row_all
            if update:
##                updateCur.updateRow(row)
                count += 1
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
