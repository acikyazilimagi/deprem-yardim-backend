# Standard Library
import json

# Third Party
import requests

class TY_BFF:
    def __init__(self, api_url):
        self.session = requests.session()
        self.api_url = api_url

    def request(self, address):
        response = self.session.get(self.api_url, params={"address": address.lower()})
        if response.status_code == 200:
            return self.response(response.json(), address)
        else:
            return {
                    "address": address,
                    "latitude": 0.0,
                    "longitude": 0.0,
                    "northeast_lat": 0.0,
                    "northeast_lng": 0.0,
                    "southwest_lat": 0.0,
                    "southwest_lng": 0.0,
                    "formatted_address": "",
                    "is_resolved": False,
                    }

    def response(self, response, address):
        if geolocation_results := response.get("results", []):
            geolocations = geolocation_results
            geometries = [geolocation["geometry"] for geolocation in geolocations]
            locations = [geometry.get("location", {"lat": 0.0, "lng": 0.0}) for geometry in geometries]
            viewports = [geometry.get(
                "viewport",
                {
                    "northeast": {"lat": 0.0, "lng": 0.0},
                    "southwest": {"lat": 0.0, "lng": 0.0},
                    },
                ) for geometry in geometries]

            responses = []
            for i in range(len(geolocations)):
                response = {"address": address,
                            "latitude": locations[i]["lat"],
                            "longitude": locations[i]["lng"],
                            "northeast_lat": viewports[i]["northeast"]["lat"],
                            "northeast_lng": viewports[i]["northeast"]["lng"],
                            "southwest_lat": viewports[i]["southwest"]["lat"],
                            "southwest_lng": viewports[i]["southwest"]["lng"],
                            "formatted_address": geolocations[i]["formatted_address"],
                            "is_resolved": True
                        }
                responses.append(response)
            return responses

        else:
            return {
                "address": address,
                "latitude": 0.0,
                "longitude": 0.0,
                "northeast_lat": 0.0,
                "northeast_lng": 0.0,
                "southwest_lat": 0.0,
                "southwest_lng": 0.0,
                "formatted_address": "",
                "is_resolved": False
            }
