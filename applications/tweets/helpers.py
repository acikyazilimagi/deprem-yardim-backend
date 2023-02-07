import logging

import requests
from django.conf import settings
from rest_framework import status

from tweets.models import Tweet, Address, Location
from typing import List, Dict
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
import json

logger = logging.getLogger(__name__)

def create_address(processed_address=None,full_address=None,tweet=None):
    city = processed_address.get("city")
    allowed_cities = ["Gaziantep", "Malatya", "Batman", "Bingöl", "Elazığ", "Kilis", "Diyarbakır", "Mardin", "Siirt", "Şırnak", "Van", "Muş", "Bitlis", "Hakkari", "Adana", "Osmaniye","Hatay'"]

    if city in allowed_cities or city == None:
        return Address.objects.create(
            tweet_id=tweet.id,
            address=full_address,
            city=processed_address.get("city"),
            distinct=processed_address.get("distinct"),
            neighbourhood=processed_address.get("neighbourhood"),
            street=processed_address.get("street"),
            no=processed_address.get("no"),
            name_surname=processed_address.get("name_surname"),
            tel=processed_address.get("tel"),
        )
    
def ask_to_zekai(headers: Dict[str, str], tweet: Tweet) -> None:
    submit_url = "https://zekai.co/author-api/v1/submit-text"
    ty_geolocation_url = "https://public-sdc.trendyol.com/discovery-web-websfxgeolocation-santral/geocode"
    data = {
        "segment": "author-complete",
        "model": "text-davinci-003",
        "sentence": """Tabular Data Extraction You are a highly intelligent and accurate tabular data extractor from 
        plain text input and especially from emergency text that carries address information, your inputs can be text 
        of arbitrary size, but the output should be in [{'tabular': {'entity_type': 'entity'} }] JSON format Force it 
        to only extract keys that are shared as an example in the examples section, if a key value is not found in the 
        text input, then it should be ignored and should be returned as an empty string Have only il, ilçe, mahalle, 
        sokak, no, tel, isim_soyisim, adres Examples: Input: Deprem sırasında evimizde yer alan adresimiz: İstanbul, 
        Beşiktaş, Yıldız Mahallesi, Cumhuriyet Caddesi No: 35, cep telefonu numaram 5551231256, adim Ahmet Yilmaz 
        Output: {\"city\": \"İstanbul\", \"distinct\": \"Beşiktaş\", \"neighbourhood\": \"Yıldız Mahallesi\", \"street\": \"Cumhuriyet Caddesi\", \"no\": 35, \"tel\": \"5551231256\", \"name_surname\": \"Ahmet Yılmaz\", \"address\": \"İstanbul, Beşiktaş, Yıldız Mahallesi, Cumhuriyet Caddesi No: 35\"}
                    Input: %s
                    Output:
                    """
        % tweet.full_text,
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
    submit_response = requests.post(
        url=submit_url, json=data, headers=headers, verify=False
    )
    if submit_response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        logger.debug(f"Status code: {submit_response.status_code}")
        return

    if submit_response.status_code == status.HTTP_400_BAD_REQUEST:
        logger.debug(f"Status code: {submit_response.status_code}, payload: {data}, reason: ")
        # we should have another state in model for the failed request so that we run a task for them too.
        return

    # TODO: can this be transaction atomic?
    try:
        submit_data = submit_response.json()
    except requests.exceptions.InvalidJSONError:
        return
    if choices := submit_data.get("choices"):
        processed_address = json.loads(choices[0]["text"].strip())
        full_address = processed_address.get("address")
        # do we want to save this address when it doesn't even have address?
        if not full_address:
            return
        
        address = create_address(processed_address, full_address, tweet)
        if not address:
            return

        geolocation_response = requests.get(
            url=ty_geolocation_url, params={"address": full_address}
        )
        geolocation_data = geolocation_response.json()
        if geolocation_results := geolocation_data.get("results", []):
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
            Location.objects.create(
                address=address,
                latitude=location["lat"],
                longitude=location["lng"],
                northeast_lat=viewport["northeast"]["lat"],
                northeast_lng=viewport["northeast"]["lng"],
                southwest_lat=viewport["southwest"]["lat"],
                southwest_lng=viewport["southwest"]["lng"],
                formatted_address=geolocation["formatted_address"]
            )
            address.is_resolved = True
            address.save()


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
