### Code for deleting a domain from a geodatabase ###

import arcpy
arcpy.env.overwriteOutput = True

sRef = arcpy.SpatialReference()
sRef.factoryCode = 4326
sRef.create()

gpParams  = {
    'CreateFeatureClass':
    {'out_name':'TestFeature1', 'geometry_type':'POINT', 'spatial_reference':sRef, 'has_m':'DISABLED', 'has_z':'DISABLED'},
    
    'AddField':
    {'field_name':'FieldWithDomain', 'field_type':'DOUBLE', 'field_is_required':'REQUIRED', 'field_domain':'TestDomain'},

    'CreateDomain':
    {'domain_name':'TestDomain', 'domain_description':'Test Domain', 'field_type':'DOUBLE', 'domain_type':'CODED'},
    
    'DomainValues':
    {1:'Alpha', 2:'Bravo', 3:'Charlie', 4:'Delta'},
    
    'RemoveDomain':
    {'field_name':'FieldWithDomain'},
    
    'DeleteDomain':
    {'domain_name':'TestDomain'},

    'HydrateFeatureClass':
    {'field_names':('SHAPE@XY', 'FieldWithDomain'), 'row_values':[((0,0), 1), ((0,1), 2), ((1,0), 3), ((1,1), 4)]}}

def main():
    # Clean workspace of test feature and domain
    arcpy.env.workspace = workspace = arcpy.GetParameterAsText(0)   
    for fc in arcpy.ListFeatureClasses("*" + gpParams['CreateFeatureClass']['out_name']): 
        arcpy.Delete_management(fc)
        arcpy.AddMessage("Deleted existing feature class...")
    
    if (gpParams['CreateDomain']['domain_name'] in arcpy.Describe(workspace).Domains): 
        arcpy.DeleteDomain_management(workspace, **gpParams['DeleteDomain'])
        arcpy.AddMessage("Deleted existing domain...")
        
    # Create feature class in workspace
    arcpy.AddMessage("Creating feature class...")
    featClass = arcpy.CreateFeatureclass_management(workspace, **gpParams['CreateFeatureClass']).getOutput(0)
    
    # Create Domain
    arcpy.AddMessage("Creating domain...")
    arcpy.CreateDomain_management(workspace, **gpParams['CreateDomain'])
    
    # Populate Domain
    arcpy.AddMessage("Hydrating Domain")
    for code, desc in gpParams['DomainValues'].items():
        arcpy.AddCodedValueToDomain_management(workspace, gpParams['CreateDomain']['domain_name'], code, desc)

    # Assign Domain to Feature Class
    arcpy.AddMessage("Adding domain to feature...")
    arcpy.AddField_management(featClass, **gpParams['AddField'])

    # Register Feature Class as Versioned
    arcpy.AddMessage("Hydrating feature...")
    arcpy.RegisterAsVersioned_management(featClass)    
    
    # Hydrate Feature Class
    if arcpy.GetInstallInfo('Desktop')['Version'] in (u'10.1', u'10.2'):
        from arcpy import da
        edit = da.Editor(workspace)
        edit.startEditing(False, True)
        edit.startOperation()
        
        try:
            with da.InsertCursor(featClass, gpParams['HydrateFeatureClass']['field_names']) as cursor:
                for row in gpParams['HydrateFeatureClass']['row_values']:
                    cursor.insertRow(row)
                del row
        except: 
            edit.abortOperation()
            edit.stopEditing(False) 
            return
        finally:
            edit.stopOperation()
            edit.stopEditing(True)
        
    else:
        point = arcpy.Point()
        rows  = arcpy.InsertCursor(featClass)
        for pnt, val in gpParams['HydrateFeatureClass']['row_values']:
            row = rows.newRow()
            point.X = pnt[0]; point.Y = pnt[1]
            pointGeom = arcpy.PointGeometry(point, gpParams['CreateFeatureClass']['spatial_reference'])
            row.setValue('Shape', pointGeom)
            row.setValue(gpParams['AddField']['field_name'], val)
        
        del row; del rows; del point; del pointGeom
    
    # Attempt to delete domain while in use
    try:
        arcpy.AddMessage("

Deleting a domain this is in use.
***This should return an error***")
        arcpy.DeleteDomain_management(workspace, **gpParams['DeleteDomain'])
        arcpy.AddMessage(arcpy.GetMessages())
    except: arcpy.AddMessage(arcpy.GetMessages(2))
    
    # Remove domain from feature class
    domainFields = [f.name for f in arcpy.ListFields(featClass) if f.domain == gpParams['CreateDomain']['domain_name']]
    for domainField in domainFields: arcpy.RemoveDomainFromField_management(featClass, **gpParams['RemoveDomain'])
        
    # Attempt to delete domain while not in use
    try:
        arcpy.AddMessage("

Deleting domain that is not in use")
        arcpy.DeleteDomain_management(workspace, **gpParams['DeleteDomain'])
        arcpy.AddMessage(arcpy.GetMessages())
    except: arcpy.AddMessage(arcpy.GetMessages(2))    

    # Delete features used for testing
    arcpy.AddMessage("

Deleting feature used for testing")
    arcpy.Delete_management(featClass)

if __name__ == '__main__':
    main()



### Code for deleting coded values from a domain ###

import arcpy
arcpy.env.overwriteOutput = True

sRef = arcpy.SpatialReference()
sRef.factoryCode = 4326
sRef.create()

gpParams  = {
    'CreateFeatureClass':
    {'out_name':'TestFeature1', 'geometry_type':'POINT', 'spatial_reference':sRef, 'has_m':'DISABLED', 'has_z':'DISABLED'},
    
    'AddField':
    {'field_name':'FieldWithDomain', 'field_type':'DOUBLE', 'field_is_required':'REQUIRED', 'field_domain':'TestDomain'},

    'CreateDomain':
    {'domain_name':'TestDomain', 'domain_description':'Test Domain', 'field_type':'DOUBLE', 'domain_type':'CODED'},
    
    'DomainValues':
    {1:'Alpha', 2:'Bravo', 3:'Charlie', 4:'Delta'},
    
    'RemoveDomain':
    {'field_name':'FieldWithDomain'},
    
    'DeleteDomain':
    {'domain_name':'TestDomain'},

    'HydrateFeatureClass':
    {'field_names':('SHAPE@XY', 'FieldWithDomain'), 'row_values':[((0,0), 1), ((0,1), 2), ((1,0), 3), ((1,1), 4)]}}

def main():
    # Clean workspace of test feature and domain
    arcpy.env.workspace = workspace = arcpy.GetParameterAsText(0)   
    for fc in arcpy.ListFeatureClasses("*" + gpParams['CreateFeatureClass']['out_name']): 
        arcpy.Delete_management(fc)
        arcpy.AddMessage("Deleted existing feature class...")
    
    if (gpParams['CreateDomain']['domain_name'] in arcpy.Describe(workspace).Domains): 
        arcpy.DeleteDomain_management(workspace, **gpParams['DeleteDomain'])
        arcpy.AddMessage("Deleted existing domain...")
        
    # Create feature class in workspace
    arcpy.AddMessage("Creating feature class...")
    featClass = arcpy.CreateFeatureclass_management(workspace, **gpParams['CreateFeatureClass']).getOutput(0)
    
    # Create Domain
    arcpy.AddMessage("Creating domain...")
    arcpy.CreateDomain_management(workspace, **gpParams['CreateDomain'])
    
    # Populate Domain
    arcpy.AddMessage("Hydrating Domain")
    for code, desc in gpParams['DomainValues'].items():
        arcpy.AddCodedValueToDomain_management(workspace, gpParams['CreateDomain']['domain_name'], code, desc)

    # Assign Domain to Feature Class
    arcpy.AddMessage("Adding domain to feature...")
    arcpy.AddField_management(featClass, **gpParams['AddField'])

    # Register Feature Class as Versioned
    arcpy.AddMessage("Hydrating feature...")
    arcpy.RegisterAsVersioned_management(featClass)    
    
    # Hydrate Feature Class
    if arcpy.GetInstallInfo('Desktop')['Version'] in (u'10.1', u'10.2'):
        from arcpy import da
        edit = da.Editor(workspace)
        edit.startEditing(False, True)
        edit.startOperation()
        
        try:
            with da.InsertCursor(featClass, gpParams['HydrateFeatureClass']['field_names']) as cursor:
                for row in gpParams['HydrateFeatureClass']['row_values']:
                    cursor.insertRow(row)
                del row
        except: 
            edit.abortOperation()
            edit.stopEditing(False) 
            return
        finally:
            edit.stopOperation()
            edit.stopEditing(True)
        
    else:
        point = arcpy.Point()
        rows  = arcpy.InsertCursor(featClass)
        for pnt, val in gpParams['HydrateFeatureClass']['row_values']:
            row = rows.newRow()
            point.X = pnt[0]; point.Y = pnt[1]
            pointGeom = arcpy.PointGeometry(point, gpParams['CreateFeatureClass']['spatial_reference'])
            row.setValue('Shape', pointGeom)
            row.setValue(gpParams['AddField']['field_name'], val)
        
        del row; del rows; del point; del pointGeom
    
    # Attempt to remove coded values from domain
    try:
        arcpy.AddMessage("

Removing coded values from domain")
        arcpy.DeleteCodedValueFromDomain_management(workspace, gpParams['CreateDomain']['domain_name'], gpParams['DomainValues'].keys())
        arcpy.AddMessage(arcpy.GetMessages())
    except: arcpy.AddMessage(arcpy.GetMessages(2))

    # Delete features used for testing
    arcpy.AddMessage("

Deleting feature used for testing")
    arcpy.Delete_management(featClass)
    
    # Attempt to delete domain while not in use
    try:
        arcpy.AddMessage("

Deleting domain that is not in use")
        arcpy.DeleteDomain_management(workspace, **gpParams['DeleteDomain'])
        arcpy.AddMessage(arcpy.GetMessages())
    except: arcpy.AddMessage(arcpy.GetMessages(2))        

if __name__ == '__main__':
    main()

	
	
	