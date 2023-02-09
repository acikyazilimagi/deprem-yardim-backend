# Applications
from core.helpers.google_geocode_api import GoogleGeocodeAPI
from core.helpers.regex_api import ExtractInfo
from core.helpers.ner_api import NerApi

import pandas as pd
import joblib

# Django Stuff
from django.conf import settings

DATA_PATH = settings.APPLICATIONS_DIR / "core" / "helpers" / "data"



class AddressAPI:
    def __init__(self):
        self.google_api = GoogleGeocodeAPI(settings.GOOGLE_API_KEY)

        sehir_data = pd.read_csv(str(DATA_PATH / "il_ilce_v3.csv"))
        kp_dict = joblib.load(str(DATA_PATH / "sehir_kp_objs.joblib"))
        sehir_dict = joblib.load(str(DATA_PATH / "sehir_dict.joblib"))
        self.regex_api = ExtractInfo(kp_dict, sehir_dict, sehir_data)

        self.ner_url = "https://api-inference.huggingface.co/models/deprem-ml/deprem-ner"
        self.ner_api = NerApi(self.ner_url, settings.HF_API_KEY)

    def google_geocode_api_request(self, address_text: str):
        return self.google_api.request(address_text)

    def regex_api_request(self, address_text: str):
        return self.regex_api.extract(address_text)

    def ner_api_request(self, address_text: str):
        return self.ner_api.query(address_text)