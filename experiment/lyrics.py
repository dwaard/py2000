import requests, urllib
from requests_oauthlib import OAuth1
import xmltodict
import collections


def dumpclean(obj, prefix=''):
    if type(obj) == dict or type(obj) == collections.OrderedDict:
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print prefix + k
                dumpclean(v, prefix + "    ")
            else:
                print '%s%s : %s' % (prefix, k, v)
    elif type(obj) == list:
        for v in obj:
            if hasattr(v, '__iter__'):
                dumpclean(v)
            else:
                print v
    else:
        print obj


consumer_key = '5757d6465605f07dff5d93f997ef2f6feb42db4a'
consumer_secret = 'ea4d7a3b65cd333462e7e2756bd3bab69193dd12'
oauth_access_token = '07e2989f75b944ac9d92ecce740d552d9badcc77'
oauth_token_secret = 'afcfa8fe29654e24d0a4ab8791cf82c0fb2912cb'

artist = "Prince"
title = "Purple Rain"

url = 'http://api.music-story.com/en/track/search?artist=%s&title=%s' % (artist, title)
auth = OAuth1(consumer_key, consumer_secret,
              oauth_access_token, oauth_token_secret,
              signature_type='query')

data = xmltodict.parse(requests.get(url, auth=auth).text)
print(dumpclean(data))