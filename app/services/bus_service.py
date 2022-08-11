from config import db
from werkzeug.exceptions import NotFound
from math import radians, cos, sin, asin, sqrt
import geopy.distance
from cachetools import cached, TTLCache

from models.bus_route import BusRoute
from models.bus_stop import BusStop

cache = TTLCache(maxsize=100, ttl=86400)

def get_all_stops():
    '''
    Get all entities
    :returns: all entity
    '''
    stops = BusStop.query.all()
    return stops

def get_all_routes():
    '''
    Get all entities
    :returns: all entity
    '''
    stops = BusRoute.query.all()
    return stops

def post_stop(body):
    '''
    Create entity with body
    :param body: request body
    :returns: the created entity
    '''
    bus_stop = BusStop(**body)
    #is_bus_stop_valid = validate_bus_stop_body(bus_stop)
    db.session.add(bus_stop)
    db.session.commit()
    return bus_stop

def post_route(body):
    '''
    Create entity with body
    :param body: request body
    :returns: the created entity
    '''
    bus_route = BusRoute(**body)
    db.session.add(bus_route)
    db.session.commit()
    return bus_route

def put_stop(body):
    '''
    Update entity by id
    :param body: request body
    :returns: the updated entity
    '''
    bus_stop = BusStop.query.get(body['id'])
    if bus_stop:
        bus_stop = BusStop(**body)
        db.session.merge(bus_stop)
        db.session.flush()
        db.session.commit()
        return bus_stop
        
    raise NotFound('no such entity found with id=' + str(body['id']))

def delete_stop(id):
    '''
    Delete entity by id
    :param id: the entity id
    :returns: the response
    '''
    bus_stop = BusStop.query.get(id)
    if bus_stop:
        db.session.delete(bus_stop)
        db.session.commit()
        return {'success': True}
    raise NotFound('no such entity found with id=' + str(id))

def get_min_distance_stops(stops, curr_lat, curr_long, num_stops=3):
    '''
    Calculate distances between current location and bus stops in DB
    : returns the closest 3 (default) bus stops of current location
    '''
    min_dist_stops = []
    stops = [stop.as_dict() for stop in stops]
    if not stops or not curr_lat or not curr_long: return -1
    
    # calculate distance between current location and bus stops 
    for stop in stops:
        dist_from_curr = geodesic_dist_calculate(curr_lat, curr_long, stop['latitude'], stop['longitude'])
        stop['dist_from_curr_location'] = dist_from_curr

    # sort stops list by distance key calculated above 
    ordered_stops = sorted(stops, key=lambda d: d['dist_from_curr_location']) 
    
    # filter results to only return selective keys
    req_key_list = ['stopname', 'dist_from_curr_location']
    for stop in ordered_stops[:num_stops]:
        min_dist_stops.append({key: value for (key, value) in stop.items() if key in req_key_list})

    return min_dist_stops

def geodesic_dist_calculate(clat, clong, lat, long):
    '''
    Gets two latitude-longitude pairs
    : returns geodesic distance in miles between two latitude-longitude pairs
    '''
    distance = geopy.distance.geodesic([clat, clong], [lat, long]).miles
    return distance

def haversine(lon1, lat1, lon2, lat2):
    '''
    Get haversine distance (takes earth's curvature into consideration) between two sets of 
    latitude-longitude pairs
    : returns distance in miles between them
    '''
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3959 # Radius of earth in miles. Use 6371 for kilometers. Determines return value units.
    return c * r