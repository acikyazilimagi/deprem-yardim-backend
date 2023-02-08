# Standard Library
import json

# Third Party
import requests

class AddressEvaluator():

    def __init__(self):
        self.session = requests.session()
        self.tr_geolocation_centre = {
                "ne_lat":43.25302605909373,
                "ne_lng":42.705981743884905,
                "sw_lat":32.846986448244536,
                "sw_lng":29.700645139879093
                }
        self.afetharita_litearea_api_url = "https://api.afetharita.com/feeds/areas-lite?ne_lat={}&ne_lng={}&sw_lat={}&sw_lng={}".format(self.tr_geolocation_centre["ne_lat"], self.tr_geolocation_centre["ne_lng"], self.tr_geolocation_centre["sw_lat"], self.tr_geolocation_centre["sw_lng"])

    def get_busiest_address(self, addresses):

        busiest_address = addresses[0]

        average_location = self.get_average_location()
        if average_location is None:
            return busiest_address

        min_difference = 999.9
        for address in addresses:
            latitude_difference = abs(address["latitude"] - average_location[0])
            longitude_difference = abs(address["longitude"] - average_location[1])
            difference = latitude_difference + longitude_difference

            if difference < min_difference:
                min_difference = difference
                busiest_address = address

        return busiest_address

    def get_average_location(self):

        response = self.session.get(self.afetharita_litearea_api_url)
        if response.status_code != 200:
            return None

        response = response.json()
        all_geolocation_count = response["count"]
        all_geolocations = response["results"]

        total_latitude = 0.0
        total_longitude = 0.0

        for geolocation in all_geolocations:

            # loc[0] ~ latitude, loc[1] ~ longitude according to Location model
            latitude = geolocation["loc"][0]
            longitude = geolocation["loc"][1]

            total_latitude += latitude
            total_longitude += longitude

        average_latitude = total_latitude / all_geolocation_count
        average_longitude = total_longitude / all_geolocation_count

        return [average_latitude, average_longitude]
