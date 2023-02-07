from core.helpers.trendyol_bff import TY_BFF
from core.helpers.regex_api import ExtractInfo


class AddressAPI:
    def __init__(self):
        self.ty_geolocation_url = "https://public-sdc.trendyol.com/discovery-web-websfxgeolocation-santral/geocode"
        self.ty_api = TY_BFF(self.ty_geolocation_url)
        
        self.regex_api = ExtractInfo()
        
    def trendyol_bff_api_request(self, address_text: str):
        return self.ty_api.request(address_text)
        
    def regex_api_request(self, address_text: str):
        return self.regex_api.extract(address_text)
