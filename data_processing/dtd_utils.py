import math
import json
import numpy as np

def airport_distance(airport_data, airport_name_1, airport_name_2):
    if 'local' == str(airport_name_1).lower() or 'local' == str(airport_name_2).lower():
        return 0
    
    if not isinstance(airport_name_1, str) or not isinstance(airport_name_2, str):
        return 0

    airport1 = airport_data[airport_name_1]
    airport2 = airport_data[airport_name_2]

    lat1 = airport1['lat']
    lon1 = airport1['lon']
    lat2 = airport2['lat']
    lon2 = airport2['lon']

    dist = lat_long_distance(lat1, lon1, lat2, lon2)
    return round(dist, 2)

def lat_long_distance(lat1, lon1, lat2, lon2):
    R = 3958.76  # Earth radius in miles
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.int32):
            return int(obj)
        if isinstance(obj, np.int64):
            return int(obj)
        return json.JSONEncoder.default(self, obj)