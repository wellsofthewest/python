from instagram.client import InstagramAPI
import urllib

client_id = "f98a677d61524d81a2d362ceb831f2b2"
client_secret = "8c8a038afccf4a5ab00e8b438b3c8c65"

api = InstagramAPI(client_id=client_id, client_secret=client_secret)
##ynp_media = api.tag_search('yosemite')
##print ynp_media

cnt = 0
med_ids, next = api.tag_recent_media(tag_name='cloudsrest', count=10)
for media in med_ids:
    picUrl = media.images['standard_resolution'].url
    urllib.urlretrieve(picUrl, r'C:\temp\test{}.jpg'.format(cnt))
    cnt += 1