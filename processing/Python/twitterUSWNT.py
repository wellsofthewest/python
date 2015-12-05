import twitter, os, arcpy, string
from twitter import *

term = raw_input('Search Term: ')

gdb = r"Database Connections\Connection to cwellsrhel.sde"

#conn = arcpy.ArcSDESQLExecute(gdb)

MY_TWITTER_CREDENTIALS = os.path.expanduser('~/.my_app_credentials')
if not os.path.exists(MY_TWITTER_CREDENTIALS):
    oauth_dance("PythonApp_geogedu", 'EUxV6WCR4YfiqC3aQwIJuRDkA', 'IJBtIzzEaiL1LKoL2pcjCkHJPNAL7sg8GH7jDJyo9Lq1eZ9eMI',
                MY_TWITTER_CREDENTIALS)

oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDENTIALS)

twitter = Twitter(auth=OAuth(
    oauth_token, oauth_secret, 'EUxV6WCR4YfiqC3aQwIJuRDkA', 'IJBtIzzEaiL1LKoL2pcjCkHJPNAL7sg8GH7jDJyo9Lq1eZ9eMI'))

sql = """insert into uswnt_tweets values ('{0}', {1}, {2}, '{3}', '{4}', '{5}', sde.st_geometry({6}, {7}, null, null, 4326), '{8}')"""

list = []
for pages in range(1, 10):
    if pages == 1:
        search = twitter.search.tweets(q=term, geocode='34.05,-118.25,1000mi', count=100, result_type='recent')
        for i in search['statuses']:
            coord = i.get('coordinates')
            if coord is not None:
                list.append(i.get('id'))
                id = i.get('id')
                x = coord['coordinates'][0]
                y = coord['coordinates'][1]
                tweet = i.get('text').replace("'", "''")
                print tweet
                uTweet = filter(lambda x: x in string.printable, tweet)
                screen_name = i.get('user').get('screen_name')
                location = i.get('location')
                plc = i.get('place')
                name = plc.get('full_name')
                print uTweet
                #conn.execute(sql.format(uTweet, y, x, screen_name, location, name, x, y, id))


    else:
        search = twitter.search.tweets(q=term, geocode='34.05,-118.25,1000mi', count=100, result_type='recent', max_id=min(list))
        for i in search['statuses']:
            coord = i.get('coordinates')
            if coord is not None:
                list.append(i.get('id'))
                id = i.get('id')
                x = coord['coordinates'][0]
                y = coord['coordinates'][1]
                tweet = i.get('text').replace("'", "''")
                print tweet
                uTweet = filter(lambda x: x in string.printable, tweet)
                screen_name = i.get('user').get('screen_name')
                location = i.get('location')
                plc = i.get('place')
                name = plc.get('full_name')
                print uTweet
                #conn.execute(sql.format(uTweet, y, x, screen_name, location, name, x, y, id))

