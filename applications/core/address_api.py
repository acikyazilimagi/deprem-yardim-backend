# Applications
from core.helpers.trendyol_bff import TY_BFF
from core.helpers.regex_api import ExtractInfo
from core.helpers.address_evaluator import AddressEvaluator

class AddressAPI:
    def __init__(self):
        self.ty_geolocation_url = "https://public-sdc.trendyol.com/discovery-web-websfxgeolocation-santral/geocode"
        self.ty_api = TY_BFF(self.ty_geolocation_url)

        self.regex_api = ExtractInfo()

        self.address_evaluator = AddressEvaluator()

    def trendyol_bff_api_request(self, address_text: str):
        addresses = self.ty_api.request(address_text)
        busiest_address = self.address_evaluator.get_busiest_address(addresses)
        return busiest_address

    def regex_api_request(self, address_text: str):
        return self.regex_api.extract(address_text)
