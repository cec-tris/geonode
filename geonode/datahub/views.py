
from geonode.utils import get_headers, http_client,json_response
from django.conf import settings
from rest_framework import status
from django.http import HttpResponse

import json

TIMEOUT = 30

__datahub_url = settings.DATAHUB_URL


def getdata(request, dataid, status=status):
    if (not request.user or not request.user.is_authenticated):
        return HttpResponse("User is not authenticated",status=status.HTTP_403_FORBIDDEN)
    
    if (not settings.DATAHUB_URL):
        return HttpResponse("DATAHUB_URL is empty",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #img url : https://dev.opendata.tris.vn/api/preview/images/
    #access_token = __get_datahub_accesstoken()
    headers = {
        #"Authorization": f"Bearer {access_token}"
    }

    #[CHUNO] remove default dataid
    dataid = settings.DATAHUB_TEST_DEFAULT_ID if settings.DATAHUB_TEST_DEFAULT_ID else dataid
    url = f"{__datahub_url}api/gishub-mapping/get-object/{dataid}"
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
        'data': data,
        'dataid': dataid,
        #**realdata
    })
realdata = {
    "link": "dev.opendata.tris.vn/public/mapping-gishub-object?id=0a259c26-4a84-4bc1-a6b3-fafc401bd4ce",
    "fields": [{
            "label": "12345678",
            "type": "folder",
            "value": {
                "url": "dev.opendata.tris.vn/data-management?folder=35491f10-f194-4f15-9d1d-27b7356d70dd",
                "name": "12345678"
            }
        }, {
            "label": "list name1.txt",
            "type": "file",
            "value": {
                "name": "list name1.txt",
                "url": "dev.opendata.tris.vn/view-file?id=f78010b1-679d-4144-aa3c-bc3a771de476",
                "thumbnailUrl": "d51a9b004d409bc7aa59888861cfa8c5-1024x1024.jpeg",
                "mimetype": "text/plain"
            }
        }, {
            "label": "screencapture-localhost-4200-dashboard-2023-11-30-16_27_02.png",
            "type": "file",
            "value": {
                "name": "screencapture-localhost-4200-dashboard-2023-11-30-16_27_02.png",
                "url": "dev.opendata.tris.vn/view-file?id=16158255-e243-4917-9de2-7c70c8ad0b76",
                "thumbnailUrl": "5a42f60ceda046e84eeb9268c7859a57-1024x1024.jpeg",
                "mimetype": "image/png"
            }
        }, {
            "label": "file-sample_100kB (1).doc",
            "type": "file",
            "value": {
                "name": "file-sample_100kB (1).doc",
                "url": "dev.opendata.tris.vn/view-file?id=4c387e51-b4c4-4896-8f19-25210b773b8d",
                "thumbnailUrl": "983883bc4412db24219bb8b5ddfb48fc-1024x1024.jpeg",
                "mimetype": "application/msword"
            }
        }, {
            "label": "MobiFone 2022.xlsx",
            "type": "file",
            "value": {
                "name": "MobiFone 2022.xlsx",
                "url": "dev.opendata.tris.vn/view-file?id=ab0fc0e5-6c87-43f2-ad8a-dc5d14edc533",
                "thumbnailUrl": "af3a7992bf3783f84a2acc2ef1cb70ab-1024x1024.jpeg",
                "mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            }
        }, {
            "label": "New Text Document.txt",
            "type": "file",
            "value": {
                "name": "New Text Document.txt",
                "url": "dev.opendata.tris.vn/view-file?id=e4efa4be-9a03-4032-922d-8756ddc7e370",
                "thumbnailUrl": "2535af95d81a9f066468541bfc2b4b27-1024x1024.jpeg",
                "mimetype": "text/plain"
            }
        }
    ]
}

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