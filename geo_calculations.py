from haversine import inverse_haversine, Direction
import requests
from config import GOOGLE_API_KEY

def extract_lat_long_via_address(address):
    lat = lon = None
    api_key = GOOGLE_API_KEY
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = f"{base_url}?address={address}&key={api_key}"
    try:
        r = requests.get(endpoint)
        if r.status_code not in range(200, 299):
            return lat, lon

        results = r.json()['results'][0]
        lat = results['geometry']['location']['lat']
        lon = results['geometry']['location']['lng']
    except:
        pass
    
    return lat, lon


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
