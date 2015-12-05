import arcpy, os, string, re

def RefreshMxd(folderPath, mxd_temp, mxd_new):
    for filename in os.listdir(folderPath):        
        fullpath = os.path.join(folderPath, filename)            
        if os.path.isfile(fullpath):            
            basename, extension = os.path.splitext(fullpath)            
            if extension.lower() == ".mxd":                
                               
                mxd_start = arcpy.mapping.MapDocument(fullpath)
                newlyrs = arcpy.mapping.ListLayers(mxd_start)
                mxd_tmp = arcpy.mapping.MapDocument(mxd_temp)
                print fullpath
                for df in arcpy.mapping.ListDataFrames(mxd_tmp):
                    for lyr in newlyrs:
                        print  "\t"+ lyr.name, lyr.dataSource
                        arcpy.mapping.AddLayer(df, lyr, "BOTTOM")
                        print "Added layer {0}".format(lyr)
                mxd_tmp.saveACopy(mxd_new + os.sep + filename)
                    
                print "Saved mxd at {0}".format(mxd_new)
                #free memory
                del df, lyr, newlyrs, mxd_tmp, mxd_start

if __name__== "__main__":
    folderPath = r"C:\Incidents\MXD_Refresh"
    mxd_temp = r"C:\Users\chri6962\Desktop\Blank.mxd"
    mxd_new = r"C:\Incidents\MXD_New"
    if not os.path.exists(mxd_new):
        os.mkdir(mxd_new)
    RefreshMxd(folderPath, mxd_temp, mxd_new)
