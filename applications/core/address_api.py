import os

from core.helpers.trendyol_bff import TY_BFF
from core.helpers.regex_api import ExtractInfo
from core.helpers.ner_api import NerApi


class AddressAPI:
    def __init__(self):
        self.ty_geolocation_url = "https://public-sdc.trendyol.com/discovery-web-websfxgeolocation-santral/geocode"
        self.ty_api = TY_BFF(self.ty_geolocation_url)
        
        self.regex_api = ExtractInfo()

        self.ner_api_url = "https://api-inference.huggingface.co/models/deprem-ml/deprem-ner"
        self.ner_api = NerApi(self.ner_api_url, os.environ.get("NER_API_KEY"))
        
    def trendyol_bff_api_request(self, address_text: str):
        return self.ty_api.request(address_text)
        
    def regex_api_request(self, address_text: str):
        return self.regex_api.extract(address_text)


    def ner_api_request(self, address_text: str):
        return self.ner_api.request(address_text)
