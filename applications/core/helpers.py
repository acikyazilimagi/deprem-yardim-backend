from typing import List, Dict
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
import json
import requests
from rest_framework import status
from django.conf import settings
import logging


logger = logging.getLogger(__name__)


def login_to_zekai():
    login_url = "https://zekai.co/api/v1/login/"
    login_response = requests.post(
        url=login_url,
        json={"username": settings.ZEKAI_USERNAME, "password": settings.ZEKAI_PASSWORD},
    )
    login_data = login_response.json()
    access_token = login_data.get("access_token")
    csrf_token = login_response.cookies.get("csrftoken")
    headers = {"Authorization": f"Bearer {access_token}", "X-CSRFToken": csrf_token}
    return headers


def analyze_with_zekai(headers: Dict[str, str], text: str):
    submit_url = "https://zekai.co/author-api/v1/submit-text"
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
        % text,
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
        logger.debug(
            f"Status code: {submit_response.status_code}, payload: {data}, reason: "
        )
        # we should have another state in model for the failed request so that we run a task for them too.
        return

    # TODO: can this be transaction atomic?
    try:
        submit_data = submit_response.json()
        return submit_data
    except requests.exceptions.InvalidJSONError:
        return
