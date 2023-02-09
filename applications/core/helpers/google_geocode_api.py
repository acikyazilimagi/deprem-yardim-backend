import json
import requests
import pandas as pd
from googlemaps import Client as GoogleMaps
import googlemaps
import gmaps
import urllib.parse

class GoogleGeocodeAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        
    def request(self, address):
        encoded_address = urllib.parse.urlencode({'query':address_text})
        response = requests.get(f'https://maps.googleapis.com/maps/api/place/textsearch/json?{encoded_address}&inputtype=textquery&fields=formatted_address,name,geometry&key={self.api_key}')
        if response.status_code == 200:
            return self.response(response.json(), address)
        else:
            return {
                'address': address,
                'latitude': 0.0,
                'longitude': 0.0,
                'northeast_lat': 0.0,
                'northeast_lng': 0.0,
                'southwest_lat': 0.0,
                'southwest_lng': 0.0,
                'formatted_address': '',
                'is_resolved': False
            }
        
    def response(self, response, address):
        if geolocation_results := response.get("results", []):
            geolocation = geolocation_results[0]
            geometry = geolocation["geometry"]
            location = geometry.get("location", {"lat": 0.0, "lng": 0.0})
            viewport = geometry.get(
                "viewport",
                {
                    "northeast": {"lat": 0.0, "lng": 0.0},
                    "southwest": {"lat": 0.0, "lng": 0.0},
                },
            )

            return {
                'address': address,
                'latitude': location["lat"],
                'longitude': location["lng"],
                'northeast_lat': viewport["northeast"]["lat"],
                'northeast_lng': viewport["northeast"]["lng"],
                'southwest_lat': viewport["southwest"]["lat"],
                'southwest_lng': viewport["southwest"]["lng"],
                'formatted_address': geolocation["formatted_address"],
                'is_resolved': True
            }
        else:
            return {
                'address': address,
                'latitude': 0.0,
                'longitude': 0.0,
                'northeast_lat': 0.0,
                'northeast_lng': 0.0,
                'southwest_lat': 0.0,
                'southwest_lng': 0.0,
                'formatted_address': '',
                'is_resolved': False
            }