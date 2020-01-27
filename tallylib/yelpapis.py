# tallylib/yelpapis.py
import json
import requests
from django.conf import settings


class YelpAPIKeys():
    def __init__(self):
        self.url = ""
        self.list = []
        self.getList()

    def getList(self):
        if settings.URL_YELP_API_KEYS is None \
            or len(settings.URL_YELP_API_KEYS) == 0:
            return
        self.url = settings.URL_YELP_API_KEYS
        for _ in range(5): # try 5 times if failed
            try:
                response = requests.get(self.url, timeout=5)
                if response.status_code != 200:
                    print("Retrieving API keys status code:", response.status_code)
                    time.sleep(1)
                else:
                    self.list = response.json()
                    print(f"Retrieved {len(self.list)} keys for the Yelp API key list.")
                    break
            except:
                self.list = []
                print("Failed to retrieve Yelp API keys.")

    def getKey(self):
        # {"Client ID":"*", "API Key":"*"},{*}...]
        key = self.list[0]['API Key']
        headers = dict()
        headers["Authorization"] = "Bearer " + key
        # rotate the list
        self.list = self.list[1:] + self.list[:1]

        return headers
    
    def removeKey(self): # Not in use 
        self.list = self.list[1:]


# this object runs in a thread inside the application process
yelp_api_keys = YelpAPIKeys()


# JSON format returned
""" 
{
    "businesses": [
        {
            "id": "WHRHK3S1mQc3PmhwsGRvbw",
            "alias": "bibble-and-sip-new-york-2",
            ...
        }
    ]
    "total": 3000,
    "region": {
        "center": {
            "longitude": -73.99429321289062,
            "latitude": 40.70544486444615
        }
    }
} 
"""
def getBusinessesViaAPI(location="NYC",
                        categories="cafe,coffee"):
    """
    Get business IDs in a location for certain categories   
    """
    headers = yelp_api_keys.getKey()
    api_base = "https://api.yelp.com/v3/businesses/search"
    url = api_base\
        + f"?location={location}" \
        + f"&categories={categories}" \
        + "&limit=1"

    # get total number of business IDs
    for _ in range(5): # try 5 times
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            biz_search = response.json()
            total = biz_search["total"]
            break
        else:
            time.sleep(1)
    
    # get business IDs
    # returns 50 IDs per request * math.ceil(total/50) requests
    offset = 0
    for _ in range(3000): # set a cap of total requests
        url = api_base\
            + f"?location={location}" \
            + f"&categories={categories}" \
            + f"&offset={offset}" \
            + "&limit=50"

        # request the API    
        biz_search = dict()
        for _ in range(5): # try 5 times
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                biz_search = response.json()
                break
            else:
                time.sleep(1)

        # break if nothing returns
        if 'businesses' not in biz_search:
            break

        # get business information
        businesses = biz_search['businesses']
        for business in businesses:
            print(business['id'])
            print(business['alias'])
            break

        break # for testing






    
