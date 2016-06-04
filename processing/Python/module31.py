#txt = r'"C:\Program Files\ArcGIS\DataStore\tools\configuredatastore.bat" https://{}.uc.esri.com:6443/arcgis admin admin c:\data'
txt = 'https://{0}.uc.esri.com:6443/arcgis'

compList = [
'0133TECHSUPP',
'0134TECHSUPP',
'0135TECHSUPP',
'0136TECHSUPP',
'0137TECHSUPP',
'0138TECHSUPP',
'0139TECHSUPP',
'0140TECHSUPP',
'0141TECHSUPP',
'0142TECHSUPP',
'0143TECHSUPP',
'0144TECHSUPP',
'0145TECHSUPP',
'0146TECHSUPP']

for machine in compList:
    print txt.format(machine)