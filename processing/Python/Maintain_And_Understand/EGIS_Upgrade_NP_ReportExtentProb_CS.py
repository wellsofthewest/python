import arcpy, os, time,json, sys

GDBToProcess = arcpy.GetParameterAsText(0)

wrkspc = r'G:\Projects\AmericanWater\GDBUpgrade'
sdeDir = wrkspc + '\SDE Connections'


DBS = ''
workspace = ''
dataList = []


#sdelist = os.listdir(sdeDir)

def doWork(InputData):

	global dataList
	
	for DB in DBS:

		theDB = DB[-(len(DB)-4):]
		print "Processing " + DB
		
		dataList = []
		sde = DB+'-SDE.sde'			#create sde connection from DB name
		fullsde = os.path.join(sdeDir, sde)     #add the full directory path
		# print fullsde
		
		buildDataList(fullsde,theDB)		#build a list of all the objects in the DB


		getExtentProbs(fullsde,dataList)              #post-compress analyze		


def buildList(InputData):
	print time.strftime("%Y%m%d_%H%M%S") + ' - running buildList ' 
	buildList = InputData.split(";")
	global DBS
	DBS = buildList	
				
def buildDataList(fullsde,theDB):
	print time.strftime("%Y%m%d_%H%M%S") + ' - running buildDataList '
	global workspace

	workspace = fullsde
	arcpy.env.workspace = workspace
	try:
		desc = arcpy.Describe(arcpy.env.workspace)
		# print desc.workspaceType
	except:
		print "Database connection specified, " + fullsde + ' Not Found'
		sys.exit()
		
	#start with free feature classes
	global dataList
	dataList = arcpy.ListTables() + arcpy.ListFeatureClasses()
	#add features classes within featuredatasets
	for dataset in arcpy.ListDatasets("", "Feature"):
		# print dataset
		theFDList = dataset.split('.')
		theFD = theFDList[1] + '.' + theFDList[2]

		arcpy.env.workspace = os.path.join(workspace, dataset)
		dataList += arcpy.ListFeatureClasses()
	# print '....Number of items to process = ' + str(len(dataList))
    
def roundIt(theNum):
	theIntNum = int(theNum)
	rFact = '4' + '9'*(len(str(theIntNum))-2)
	if rFact == '4':
		rFact = '0'
	theFinalNum = int(round((theIntNum + int(rFact)),-(len(str(theIntNum))-1)))
	return theFinalNum
    
def getExtentProbs(fullsde,datalist):
	arcpy.env.workspace = fullsde
	desc = arcpy.Describe(arcpy.env.workspace)
	# print desc.workspaceType
	# if desc.workspaceType == 'RemoteDatabase':
	# 	sdeConn = True
	#else:
	#	sdeConn = False
	#	theGDBParts = arcpy.env.workspace.split('\\')
	#	theGDB = theGDBParts[len(theGDBParts)-1]
	#	aFilePath = arcpy.env.workspace.split(theGDB)[0]
	#	print theGDB
	#	print aFilePath

	egdb = arcpy.env.workspace
	egdb_conn = arcpy.ArcSDESQLExecute(egdb)


	sql = '''select l.owner,l.table_name,i.name,l.minx, l.maxx, l.miny, l.minx,
		CASE when l.maxx < l.minx THEN 0 else (l.maxx - l.minx) END as FC_Width,
		CASE when l.maxy < l.miny THEN 0 else (l.maxy - l.miny) END as FC_Height,
		(t.bounding_box_xmax - t.bounding_box_xmin) as SI_Width,
		(t.bounding_box_ymax - t.bounding_box_ymin) as SI_Height
		from sde.sde_layers l join
		sys.indexes i on upper(l.table_name) = upper(object_name(i.Object_id)) join
		sys.spatial_index_tessellations t on i.object_id = t.object_id
		where i.type = 4 and l.table_name not like 'GDB%';'''

	egdb_return = egdb_conn.execute(sql)

	theExtents = {}	
	for i in egdb_return:
	    theExtents[i[1]] = [roundIt(i[7]),roundIt(i[8]),roundIt(i[9]),roundIt(i[10])]
	# print str(len(theExtents.keys())) + ' Items to process'
	# print theExtents.keys()


	for FC in datalist:
	# print FC
		theFCParts = FC.split('.')
		# print theFCParts
		currExt = theExtents.get(theFCParts[2].upper())
		# print theFCParts[2] + ">>" + str(currExt)
		if currExt == None:
			# print FC + ' not a feature class - Skipped'
			X=1
		else:
			theCount = arcpy.GetCount_management(FC)
			# countNum = int(theCount.getOutput(0))
			# print '... num Features = ' + str(countNum)
			if int(theCount.getOutput(0)) > 0:
				# print countNum
				tempfc = "in_memory\\tempfc"
				arcpy.MinimumBoundingGeometry_management(FC, tempfc, "ENVELOPE", "ALL", "", "MBG_FIELDS")
				realDESC = arcpy.Describe(tempfc)
				realW = roundIt(realDESC.extent.width)
				realH = roundIt(realDESC.extent.height)
				if realW <> currExt[0] or realH <> currExt[1]:
					print FC + ',has ' + str(theCount.getOutput(0)) + \
					      ' records,mismatch Extent width= (act),' + \
					      str(realW) + ',<>(FC),' + \
					      str(currExt[0]) + ',Height = (act),' + str(realH) + \
					      ',<>(FC),' + str(currExt[1])
				arcpy.Delete_management(tempfc)
			else:
				print FC + ',Has No Data,FC Extent Width =,'+ str(currExt[0]) + ',Height=,'+str(currExt[1])
    
def main():
	global GDBToProcess
	print GDBToProcess
	if GDBToProcess == '':
		ask = raw_input(r'Enter Geodatabases Connection Name'+os.linesep)
		if ask == None:
			print 'No Name Entered - Quitting'
			sys.exit()
		else:
			GDBToProcess = ask

	InputData = GDBToProcess
	print time.strftime("%Y%m%d_%H%M%S") + ' - Starting... ' 
	buildList(InputData)
	doWork(InputData)
	print time.strftime("%Y%m%d_%H%M%S") + ' - Finished... '
    

main()
