import requests
import re
import json

url = 'https://www.buzzfeed.com/comments-api/v1/comments?content_type=buzz&content_id=5359071'

resp = requests.get(url)

json1 = resp.json()
print(json1['count'])

url = 'https://www.buzzfeed.com/content-reactions-api/v1/buzz/5359071?edition=en-us'

resp = requests.get(url)

json1 = resp.json()
print(json1['total_reactions'])

url = 'https://www.buzzfeed.com/site-component/v1/en-us/buzzstats?buzz_ids=5359071'

resp = requests.get(url)

json1 = resp.json()
print(json1['results'][0]['total'])