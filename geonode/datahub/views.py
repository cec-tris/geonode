import logging
from geonode.utils import get_headers, http_client,json_response
from django.conf import settings
from rest_framework import status
from django.http import HttpResponse
from .utils import datahub_url, get_datahub_accesstoken, datahub_fakedata
from .search import geocode as searchText
import json

TIMEOUT = 30
logger = logging.getLogger(__name__)

def getdata(request, dataid, status=status):
    if (not request.user or not request.user.is_authenticated):
        return HttpResponse("User is not authenticated",status=status.HTTP_403_FORBIDDEN)
    
    access_token = get_datahub_accesstoken()
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    #TODO: update getDataHubPath
    url = f"{datahub_url}api/user/menus"
    resp, content = http_client.request(
        url, method='GET',
        headers=headers, 
        timeout=TIMEOUT,
    )

    status = int(resp.status_code)

    data = None
    if status == 200:
        data = json.loads(content)
    # else:
    #     raise Exception(f"Could get data from {url}: {content}")
    
    return json_response({
        'dataid': dataid,
        **datahub_fakedata
    })


def geocode(request):
    params = request.GET
    #q=hoàng%20văn%20thụ&format=json&bounded=0&polygon_geojson=1&priority=5&returnFullData=false
    if 'q' not in params:
        return HttpResponse("params is in valid",status=status.HTTP_400_BAD_REQUEST)
    
    result = searchText(params['q'])
    print("result",result)
    logger.error("geocode", result)
    return json_response(body={
        'result': result
    })

def reversegeocode(request):
    params = request.GET
    return json_response({
        'params': params,
    })