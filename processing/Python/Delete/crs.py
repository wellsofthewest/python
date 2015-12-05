import arcpy
from arcpy import env

#Sql Server connection:
workspcss = r"C:\Users\ken6574\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\TESTCAD@SDE@KENG.sde"

#Oracle connection:
workspcora = r'Database Connections\Connection to cwells.sde'

#Whateves
env.workspace = workspcss


#Sql Server feature class:
featureclass1 = "Test"

#Oracle feature class:
featureclass2 = "ZIP"


def querySDESpatial(workspc, fcName):    
        conn = arcpy.ArcSDESQLExecute(workspc)
        sql = "SELECT layer_id FROM sde.layers WHERE table_name = '{0}'".format(fcName)
        sde_return = conn.execute(sql)
        print type(sde_return)
        print sde_return
      
querySDESpatial(workspcora, featureclass2)

