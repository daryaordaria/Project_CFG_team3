from haversine import inverse_haversine, Direction
from collections import namedtuple
import requests

GOOGLE_API_KEY = 'AIzaSyApyx4KbXuO-hBRceBu3LugFm-rYdAlvPQ'

def extract_lat_long_via_address(address):
    Coords = namedtuple('Coords',('lat', 'lon'))
    coords = Coords(None, None)
    
    api_key = GOOGLE_API_KEY
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = f"{base_url}?address={address}&key={api_key}"
    r = requests.get(endpoint)
    if r.status_code not in range(200, 299):
        return coords
    try:
        results = r.json()['results'][0]
        coords.lat = results['geometry']['location']['lat']
        coords.lon = results['geometry']['location']['lng']
    except:
        pass
    
    return coords


def calculate_distance(coords):
    try:
        west = inverse_haversine(coords, 10, Direction.WEST) # distance set to 10km
        east = inverse_haversine(coords, 10, Direction.EAST)
        north = inverse_haversine(coords, 10, Direction.NORTH)
        south = inverse_haversine(coords, 10, Direction.SOUTH)
        area = {"lat_min": min(north[0], south[0]), 
                "lat_max": max(north[0], south[0]),
                "lon_min": min(west[1], east[1]), 
                "lon_max": max(west[1], east[1])}
    except:
        area = False
        
    return area
