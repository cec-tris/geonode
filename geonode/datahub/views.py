
from geonode.utils import get_headers, http_client,json_response
from django.conf import settings
from rest_framework import status
from django.http import HttpResponse

import json

TIMEOUT = 30

__datahub_url = settings.DATAHUB_URL if settings.DATAHUB_URL else 'https://dev.opendata.tris.vn/'
__DATAHUB_PAT = '' #DATAHUB_PersonalAccessToken
def __get_datahub_accesstoken():
    #TODO: USE __DATAHUB_PAT to GET access_token
    # implement caching

    access_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjRGRDNBOTY3MjhFMjVFREM0NTlDNDgzOUU2OTdCMDhEQ0FCNjBFQzdSUzI1NiIsInR5cCI6ImF0K2p3dCIsIng1dCI6IlQ5T3BaeWppWHR4Rm5FZzU1cGV3amNxMkRzYyJ9.eyJuYmYiOjE2ODg2OTc5MTIsImV4cCI6MTY4ODcwMTUxMiwiaXNzIjoiaHR0cHM6Ly9pZDIudHJpcy52biIsImNsaWVudF9pZCI6Im9wZW5kYXRhNGdvdiIsInN1YiI6IjVjYmNjOTVlLTRmN2UtNDFjZC04NTdmLTcyNjJmOTliMGExYyIsImF1dGhfdGltZSI6MTY4NzQ4ODU1NywiaWRwIjoibG9jYWwiLCJzaWQiOiJBQUU0OTFDRTVBRDRBNjIwMEMxRjlEQkEyRkI2N0REMSIsImlhdCI6MTY4ODY5NzkxMiwic2NvcGUiOlsib3BlbmlkIiwicHJvZmlsZSIsImVtYWlsIiwicm9sZSIsIm9mZmxpbmVfYWNjZXNzIl0sImFtciI6WyJwd2QiXX0.coFur3w1opihS2g5WriVIKhjNVrYkFU3CjUksx7SAWfi6yParqbvWKo1tO4q_be7_VSvRJCxqAc109bPIG5Mc1tY9Aub-IGaGyqKxIr6fu-_NQF4Hqddpx2RPw_nfCegO33JrfJ19OeMBDxHqAu63PCaz7pAVHDqfdyt0r9KTZTq8fKwcKpRXghm5jsaCNAPHaY03vvy1vGBCYszSzxlZUst1O1yvKF4UWEJ4I1OrTfPrA4nxE_THKfoEmonXmxm9zuj4iMRIDAsIhFRWzv2SVCgCAe_se42N9kt1sepZYcLOAOj55dt6IQdnHOiW7CojTrduwLH2-ah5Y9DK1WYUw"
    headers = {
        "Authorization": f"PAT {__DATAHUB_PAT}"
    }
    url = f"{__datahub_url}api/user/menus"
    resp, content = http_client.request(
        url, method='GET',
        headers=headers, 
        timeout=TIMEOUT,
    )

    return access_token

def getdata(request, dataid, status=status):
    if (not request.user or not request.user.is_authenticated):
        return HttpResponse("User is not authenticated",status=status.HTTP_403_FORBIDDEN)
    
    access_token = __get_datahub_accesstoken()
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    #TODO: update getDataHubPath
    url = f"{__datahub_url}api/user/menus"
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
        'menus': data,
        'dataid': dataid,
        **fakedata
    })

fakedata = {
            'schema': {},
            'format': 'properties',  #template
            'html':'<div></div>',
            'fields': [
                {
                    'label': "Ngày ban hành",
                    'type': "text" ,
                    'value' : "20/12/1989"
                },
                {
                    'label': "Hồ sơ",
                    'type': "file" ,
                    'value' : {
                        'thumbnailUrl': "http://localhost/uploaded/thumbs/document-cd231abb-628c-45aa-96f0-f1220ebfde29-thumb-9593706f-6eab-4350-8fbf-949443b186c3.jpg",
                        'url': "http://localhost/documents/40/embed"
                    }
                },
                {
                    'label': "Hình chụp",
                    'type': "img" ,
                    'value' : {
                        'thumbnailUrl': "http://localhost/uploaded/thumbs/document-0a37db14-ce07-4e14-a1b7-88b4bd92dc6c-thumb-ed99b809-50ef-4cae-86b7-55f1757311bb.jpg",
                        'url': "http://localhost/documents/4/embed"
                    }
                },
                {
                    'label': "Trạm BTS",
                    'type': "link" ,
                    'value' : "http://localhost/documents/4/embed"
                },
                {
                    'label': "Mô tả",
                    'type': "html" ,
                    'value' : "<></>"
                },
                {
                    'label': "BTS",
                    'type': "relations",
                    'value' : [
                        {
                            'fields': [
                                {
                                    'label': "Tram",
                                    'type': "text" ,
                                    'value' : "Tên"
                                },
                            ],
                        }
                    ]
	            },
            ]
        }