import arcpy, os, string, re

def RefreshMxd(folderPath):
    for filename in os.listdir(folderPath):        
        fullpath = os.path.join(folderPath, filename)            
        if os.path.isfile(fullpath):            
            basename, extension = os.path.splitext(fullpath)            
            if extension.lower() == ".mxd":                
                               
                mxd_start = arcpy.mapping.MapDocument(fullpath)
                newlyrs = arcpy.mapping.ListBrokenDataSources(mxd_start)
                print fullpath
                for df in arcpy.mapping.ListDataFrames(mxd_start):
                    for lyr in newlyrs:
                        print  "\n\t"+ lyr.name, lyr.dataSource


if __name__== "__main__":
    #Place the path to your MXD folder between the quotes
    folderPath = r"C:\Incidents\1297026_BrokenLinks\BrknSample"
    RefreshMxd(folderPath)
