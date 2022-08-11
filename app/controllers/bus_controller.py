from flask import Flask, Blueprint, jsonify, request
from flask_api import status
from werkzeug.exceptions import HTTPException
import json

import services.bus_service as bus_service

api = Blueprint('busstops', 'busstops')

@api.route('/bus/stops', methods=['GET'])
def api_get_stops():
    ''' Get all bus stops'''
    stops = bus_service.get_all_stops()
    return jsonify([stop.as_dict() for stop in stops]), status.HTTP_200_OK

@api.route('/bus/stops/distance', methods=['GET'])
def api_get_dist_to_stop():
    ''' Get distance between two sets of latitude and longitudes '''
    args = request.args.to_dict()

    if not args or len(args)<2:
        return "Missing latitude and longitude values, recheck parameters.", status.HTTP_400_BAD_REQUEST
    if 'latitude' not in args.keys() or 'longitude' not in args.keys():
        return "Missing latitude or longitude parameters.", status.HTTP_400_BAD_REQUEST
    
    # storing current location latitude and longitude
    curr_latitude, curr_longitude = args['latitude'], args['longitude']

    # getting bus stops list from DB
    stops = bus_service.get_all_stops()
    
    # helper method to calculate distances from stops and return closest 3 stops
    min_dist_stops = bus_service.get_min_distance_stops(stops, curr_latitude, curr_longitude)
    if min_dist_stops == -1: 
        return "Internal server error due to unavailability of stops data.", status.HTTP_500_INTERNAL_SERVER_ERROR

    return min_dist_stops, status.HTTP_200_OK

@api.route('/bus/routes', methods=['GET'])
def api_get_routes():
    ''' Get all routes'''
    routes = bus_service.get_all_routes()
    return jsonify([route.as_dict() for route in routes]), status.HTTP_200_OK

@api.route('/bus/stop', methods=['POST'])
def api_post_stop():
    ''' Create bus stop'''
    bus_stop = bus_service.post_stop(request.json)
    return jsonify(bus_stop.as_dict())

@api.route('/bus/route', methods=['POST'])
def api_post_route():
    ''' Create bus route'''
    bus_route = bus_service.post_route(request.json)
    return jsonify(bus_route.as_dict())

@api.errorhandler(HTTPException)
def handle_exception(e):
    '''Return JSON format for HTTP errors and exceptions.'''
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        'success': False,
        "message": e.description
    })
    response.content_type = "application/json"
    return response