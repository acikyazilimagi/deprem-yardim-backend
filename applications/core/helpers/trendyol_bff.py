import json
import requests

class TY_BFF:
    def __init__(self, api_url):
        self.session = requests.session()
        self.api_url = api_url
        
    def request(self, address):
        response = self.session.get(self.api_url, params={'address': address.lower()})
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