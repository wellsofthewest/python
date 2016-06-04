import os

rdp = """
screen mode id:i:2
use multimon:i:0
desktopwidth:i:1080
desktopheight:i:1920
session bpp:i:32
winposstr:s:0,1,1080,451,2160,1385
full address:s:{0}
compression:i:1
keyboardhook:i:2
audiomode:i:0
redirectdrives:i:0
redirectprinters:i:0
redirectcomports:i:0
redirectsmartcards:i:0
displayconnectionbar:i:1
autoreconnection enabled:i:1
username:s:uc\demo
authentication level:i:0
prompt for credentials:i:0
negotiate security layer:i:1
alternate shell:s:
shell working directory:s:
disable wallpaper:i:0
disable full window drag:i:0
disable menu anims:i:0
disable themes:i:0
disable cursor setting:i:0
bitmapcachepersistenable:i:1
password demo
use multimon:i:0
audiocapturemode:i:0
videoplaybackmode:i:1
connection type:i:2
allow font smoothing:i:0
allow desktop composition:i:0
redirectclipboard:i:1
redirectposdevices:i:0
redirectdirectx:i:1
remoteapplicationmode:i:0
gatewayhostname:s:
gatewayusagemethod:i:4
gatewaycredentialssource:i:4
gatewayprofileusagemethod:i:0
promptcredentialonce:i:1"""


compList = ['0132TECHSUPP',
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
'0146TECHSUPP',
'0147TECHSUPP',
'0148TECHSUPP',
'0149TECHSUPP',
'0150TECHSUPP']


out = r"C:\Share\prep\rdp"

for machine in compList:
    f = open(os.path.join(out, machine + '.rdp'), 'wb+')
    f.write(rdp.format(machine))
    f.close()

