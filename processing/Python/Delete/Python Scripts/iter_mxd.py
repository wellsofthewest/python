import os,fnmatch,arcpy

arcpy.env.workspace = r"C:\Users\ken6574\Desktop"
workspace = arcpy.ListWorkspaces("*", "Folder")

for folderPath in workspace:
    for filename in os.listdir(folderPath):
        fullPath = os.path.join(folderPath, filename)
        if os.path.isfile(fullPath):
            basename, extension = os.path.splitext(fullPath)
            if extension.lower() == ".mxd":
                mxd = arcpy.mapping.MapDocument(fullPath)
                #mxd.findAndReplaceWorkspacePaths(r"C:\oldWorkspacePath", r"C:\newWorkspacePath")
                #mxd.save()
                print str(fullPath)
del mxd
print "done"
print arcpy.GetMessages()                
