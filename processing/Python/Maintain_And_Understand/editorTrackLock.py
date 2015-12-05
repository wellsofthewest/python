
import arcpy, subprocess



def ActiveUsers(instance,user,psswd, database):
    
    
    args = ['sdemon', '-o', 'info', '-I', 'users_long' ,'-i', instance, \
           '-u', user, '-p', psswd, '-D', database]

    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    output = p.stdout.read()
            
    print output


if __name__=="__main__":        
    
    instance = 'sde:sqlserver:config31227vm2'
    user = 'sde'
    psswd = 'sde'
    database = 'testsp1'
    ActiveUsers(instance,user,psswd, database)





    connFile=r"Database Connections\testsp1.sde"
    arcpy.env.workspace = connFile
    arcpy.DisconnectUser(connFile, "ALL")

    ActiveUsers(instance,user,psswd, database)



    in_dataset="line"

    #disable editor tracking
    print "begin to disable editor tracking"
    arcpy.DisableEditorTracking_management(in_dataset)

    #field calculate
    print "begin to calculate field"
    arcpy.CalculateField_management(in_dataset, "name", "\"octThird\"")

    #enable editor tracking
    print "begin to enable editor tracking"
    arcpy.EnableEditorTracking_management(in_dataset,"","", "last_editor", "last_edit_date", "ADD_FIELDS")

    print "finish enabling editor tracking"






