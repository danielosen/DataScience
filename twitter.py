# twitter api

import requests
from requests_oauthlib import OAuth1   # authorize request
from donthackme import *


auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, TOKEN, TOKEN_SECRET)

def verify_credentials():
    # api url
    url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
    verify_response = requests.get(url, auth=auth)
    assert(verify_response.status_code == 200)

def search_query(query,result_type):
    search_url = 'https://api.twitter.com/1.1/search/tweets.json'
    params = {'q': query, 'result_type': result_type}
    search_response = requests.get(search_url, params=params, auth=auth)
    assert(search_response.status_code == 200)
    return search_response



verify_credentials()



# search
query = 'data science'
result_type = 'recent'
search_response = search_query(query,result_type)

import pprint
re_json = search_response.json()
pprint.pprint( re_json['statuses'][0] )  # statuses = tweets

#re_json.get('statuses', [] ) # advanced?!
#re_json.get('statuses', [{}] )[0] # ...



# streaming api

import json
from itertools import islice
params = {'track': '#Trump'}
#params = {'track': '#python'}
r = requests.post('https://stream.twitter.com/1.1/statuses/filter.json',
      params=params, auth=auth, stream=True)
tweets = r.iter_lines()
for tweet in tweets: #islice(tweets, 20):
  if tweet:
    tmp = json.loads( tweet.decode('utf-8') )
    print(tmp['text'])
  else:
    print('Timeout.')

r.close()
