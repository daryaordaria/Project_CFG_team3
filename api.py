GOOGLE_API_KEY = 'AIzaSyApyx4KbXuO-hBRceBu3LugFm-rYdAlvPQ'
import requests

def extract_lat_long_via_address(address_or_zipcode):
    lat1, lng1 = None, None
    api_key = GOOGLE_API_KEY
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = f"{base_url}?address={address_or_zipcode}&key={api_key}"
    r = requests.get(endpoint)
    if r.status_code not in range(200, 299):
        return None, None
    try:
        results = r.json()['results'][0]
        lat1 = results['geometry']['location']['lat']
        lng1 = results['geometry']['location']['lng']
    except:
        pass
    return lat1, lng1

loc1 = extract_lat_long_via_address("Paris")
loc2 = extract_lat_long_via_address("Breslau")

import haversine as hs

def haversine(loc1, loc2):
    distance = hs.haversine(loc1, loc2)
    return distance
distance = haversine(loc1, loc2)

print(distance)