import requests
from django.conf import settings
from tweets.models import Tweet, Address
from typing import List, Dict
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
import json

def ask_to_zekai(headers: Dict[str, str], tweet: Tweet):
    submit_url = "https://zekai.co/author-api/v1/submit-text"
    data = {
        "segment": "author-complete",
        "model": "text-davinci-003",
        "sentence": """Tabular Data Extraction
                    You are a highly intelligent and accurate tabular data extractor from plain text input and especially from emergency text that carries address information, your inputs can be text of arbitrary size, but the output should be in [{'tabular': {'entity_type': 'entity'} }] JSON format

                    Force it to only extract keys that are shared as an example in the examples section, if a key value is not found in the text input, then it should be ignored and should be returned as an empty string

                    Have only il, ilçe, mahalle, sokak, no, tel, isim_soyisim, adres

                    Examples:
                    Input: Deprem sırasında evimizde yer alan adresimiz: İstanbul, Beşiktaş, Yıldız Mahallesi, Cumhuriyet Caddesi No: 35, cep telefonu numaram 5551231256, adim Ahmet Yilmaz
                    Output: [{'Tabular': '{'il': 'İstanbul', 'ilçe': 'Beşiktaş', 'mahalle': 'Yıldız Mahallesi', 'sokak': 'Cumhuriyet Caddesi', 'no': 35, 'tel': 5551231256, 'isim_soyisim': 'Ahmet Yılmaz', 'adres': 'İstanbul, Beşiktaş, Yıldız Mahallesi, Cumhuriyet Caddesi No: 35'}' }]

                    Input: %s
                    Output:
                    """ % tweet.full_text,
        "description": "default",
        "filter": "default",
        "suffix": "",
        "maxtokens": 256,
        "templature": "0.9",
        "topp": "1.0",
        "n": "1",
        "stream": "False",
        "logprobs": "0",
        "echo": "False",
        "stop": "None",
        "presencepenalty": "0.0",
        "frequencypenalty": "0.0",
        "best_of": "1",
    }
    submit_response = requests.post(url=submit_url, json=data, headers=headers, verify=False)
    try:
        submit_data = submit_response.json()
    except requests.exceptions.InvalidJSONError:
        return
    if choices := submit_data.get("choices"):
        Address.objects.create(tweet_id=tweet.id, address=choices[0]["text"].strip())


def bulk_ask_to_zekai(tweet_data: List[Tweet]):
    login_url = "https://zekai.co/api/v1/login/"
    login_response = requests.post(
        url=login_url,
        json={"username": settings.ZEKAI_USERNAME, "password": settings.ZEKAI_PASSWORD},
    )
    login_data = login_response.json()
    access_token = login_data.get("access_token")
    csrf_token = login_response.cookies.get("csrftoken")
    headers = {"Authorization": f"Bearer {access_token}", "X-CSRFToken": csrf_token}

    thread_list: List[Future] = []
    thread_pool = ThreadPoolExecutor(max_workers=5)
    for tweet in tweet_data:
        thread = thread_pool.submit(ask_to_zekai, headers=headers, tweet=tweet)
        thread_list.append(thread)

    for _ in as_completed(thread_list, timeout=4):
        pass

class TY_BFF:
    def __init__(self):
        self.session = requests.session()
        
    def request(self, address):
        response = self.session.get('https://public-sdc.trendyol.com/discovery-web-websfxgeolocation-santral/geocode', params={'address': address.lower()})
        self.x = response
        if response.status_code == 200:
            return self.response(response.json(), address)
        else:
            return {'input_adress':address, 'formatted_address': None, 'lat': None, 'long': None}
        
    def response(self, response, address):
        if len(response['results']) > 0:
            try:
                res_dict =  { 'input_adress': address, 'formatted_address': response['results'][0]['formatted_address'], 'lat': response['results'][0]['geometry']['location']['lat'], 'long':response['results'][0]['geometry']['location']['lng']}
            except KeyError:
                try:
                    res_dict =  { 'input_adress': address, 'formatted_address': response['results'][0]['formatted_address'], 'lat': response['results'][0]['geometry']['viewport']['northeast']['lat'], 'long':response['results'][0]['geometry']['viewport']['northeast']['lng']}
                except KeyError:
                    res_dict =  { 'input_adress': address, 'formatted_address': response['results'][0]['formatted_address'], 'lat': response['results'][0]['geometry']['viewport']['southwest']['lat'], 'long':response['results'][0]['geometry']['viewport']['southwest']['lng']}
            return res_dict
        else:
            return {'input_adress':address, 'formatted_address': None, 'lat': None, 'long': None}
