

import arcpy, os, string

def Resource(databases, path,text,mxdtext,outLog,mxdLog,oldschema,newschema):
    for root, dirs, files in os.walk(path):        
        for name in files:
            if name.endswith(".mxd"):            
                mxd_name = name
                fullpath = os.path.join(root,name)
                print "Evaluating {0}".format(fullpath)
                mxd = arcpy.mapping.MapDocument(fullpath)
                 
                for df in arcpy.mapping.ListDataFrames(mxd):                    
                    for lyr in arcpy.mapping.ListLayers(mxd, "", df):
                        print "Can see layer {0}".format(lyr)
                        print lyr.serviceProperties.get('Database')

                        for db,conn in databases.iteritems():
                            
                            try:
                                
                                if str(lyr.serviceProperties.get('Database'))==db:
                                    print "layer {0} in db {1}".format(lyr.datasetName, db)
                                    newSdePath = conn
                                    oldlyr = str(lyr.datasetName)
                                    print "*** old LAYER *** {0}".format(oldlyr)
                                    newlyr = oldlyr.replace(oldschema,newschema)
                                    print "*** NEW LAYER *** {0}".format(newlyr)
                                    lyr.replaceDataSource(newSdePath, "SDE_WORKSPACE", newlyr, False)                                                                                          
                                    print "Replaced {0} from mxd {1}".format(lyr.datasetName,mxd_name)
                                    print "Examining data source {0}".format(lyr.dataSource)
                                    mxdLog.write("Replaced {0} from mxd {1}".format(str(lyr.datasetName),str(mxd_name)))
                                    mxdLog.write("\n")
                                    arcpy.RefreshTOC()
                                    arcpy.RefreshActiveView()
                                    #free memory
                                    del  newSdePath
                                    
                            except:                                
                                    outLog.write("Errors: " + str(arcpy.AddError(arcpy.GetMessages(1))))
                                    outLog.write("\n")
                                    outLog.write("Errors: " + str(arcpy.AddError(arcpy.GetMessages(2))))
                                    outLog.write("\n")
                                    outLog.write("Errors: " + str(arcpy.AddError(arcpy.GetMessages(3))))
                                    outLog.write("\n")

                mxd.saveACopy(mxd_dir + os.sep + mxd_name)
                print "Saved mxd: {0}".format(mxd_name)
                mxdLog.write("Saved: {0}".format(str(mxd_name)))
                mxdLog.write("\n")


if __name__ == "__main__":
    
    #starting folder location where old mxds reside
    path = r"C:\Delete\old_mxd"
    #Path to log file
    textdir = r"C:\temp"
    mxdtextdir = r"C:\temp"
    oldschema = "sde.TEST"
    #print "*** OLD SCHEMA *** {0}".format(oldschema)
    #newschema = 'sde2."AVWORLD\RASH5801"'
    newschema = "sde2.SDE"
    #newschema = r"sde2." + "\"" + r"AVWORLD\RASH5801" + "\""
    #print "*** NEW SCHEMA *** {0}".format(newschema)
    if not os.path.exists(textdir):
        os.mkdir(text)
    if not os.path.exists(mxdtextdir):
        os.mkdir(mxdtext)        
    text = textdir + os.sep + "errorlogs.txt"
    mxdtext = mxdtextdir + os.sep + "mxdlogs.txt"
    outLog = open(text, "w")
    mxdLog = open(mxdtext, "w")
    mxd_dir = r"C:\Delete\new_mxd"
    databases = {'sde':'C:\Users\rash5801\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\sde2_new.sde'}
    Resource(databases, path,text,mxdtext,outLog,mxdLog,oldschema,newschema)
    
