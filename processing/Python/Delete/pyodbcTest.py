import pyodbc

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=cwells102;UID=sde;PWD=sde')
cursor = cnxn.cursor()

cursor.execute("update sde.SDE_server_config set num_prop_value = 300 where prop_name = 'connections'")
cnxn.commit()
