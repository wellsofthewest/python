import twitter
from twitter import *




api = twitter.Api(consumer_key='EUxV6WCR4YfiqC3aQwIJuRDkA',
                  consumer_secret='IJBtIzzEaiL1LKoL2pcjCkHJPNAL7sg8GH7jDJyo9Lq1eZ9eMI',
                  access_token_key='384951768-1R49jZMbaE0mjknnh0qjZQOiJuttlh3TZGZZ6Rkr',
                  access_token_secret='AqRivt8M6B2b8CVLgnKibunmd3LALjIEQxt7VGmcxVslN')

search = api.GetSearch("", "(-73.943430,40.669903,30mi)")
#search = api.GetSearch('USWNT', count=200)
print len(search)
for i in search:
    print i



##tweet = api.GetStatus(618471978618335232)
##print tweet

##stream = api.GetStreamFilter(track='USWNT')
##print type(stream)
##for x in stream:
##    print x

##ls = api.GetTrendsWoeid(23424977)
##for i in ls:
##    print str(i)

