
# from django.conf import settings
# from rest_framework import status
# from django.http import HttpResponse
import requests

import logging

TIMEOUT=30 #seconds
GEOCODE_KEY = '1ae88b4898ec298438b249d3db1a72af' #iotlink
#KEY = '72b33b3c84825ecec135cc66baf04068' #loc
GEOCODE_REFERER = 'maphub.dientoan.vn'
GEOCODE_URL = 'http://api.map4d.vn/sdk/place/text-search'
GEOCODE_REFERENCE_LOCATION = '10.76,106.65'
#logger = logging.getLogger(__name__)

def geocode(text):
    headers = {
        'Referer' :GEOCODE_REFERER
    }
    
    params = {
        'key' : GEOCODE_KEY,
        'text' : text
    }
    if len(GEOCODE_REFERENCE_LOCATION) > 0:
        params['location'] = GEOCODE_REFERENCE_LOCATION
    
    url = GEOCODE_URL
    resp = requests.get(
        url, 
        params=params,
        headers=headers, 
        timeout=TIMEOUT,
    ) 
    status = int(resp.status_code)
    if status != 200:
        raise Exception(f'Response status is {status}. Content: {resp.content}')
    data =  resp.json()
    if not ('result' in data):
        raise Exception(f'Error Content: {resp.content}')
    items = data['result']

    return [{
        'id': item['id'],
        'type' : 'Feature',
        'properties' : {
            'name': item['name'],
            'display_name': item['address'],
            'types': item['types']
        },
        'geometry' : {
            'type': 'Point',
            'coordinates': [item['location']['lng'], item['location']['lat']],
        } 
    } for item in items]
   

# json = geocode('quan 12')
# print(json)

