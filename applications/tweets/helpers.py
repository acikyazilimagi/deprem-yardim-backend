import requests
from django.conf import settings
from tweets.models import Tweet, Address
from typing import List, Dict
from concurrent.futures import Future, ThreadPoolExecutor, as_completed


def ask_to_zekai(headers: Dict[str, str], tweet: Tweet):
    submit_url = "https://zekai.co/author-api/v1/submit-text"
    data = {
        "segment": "author-complete",
        "model": "text-davinci-003",
        "sentence": f"Extract the address for Google Maps APi using this tweet, the address will be from Turkey: "
                    f"{tweet.full_text}",
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
        Address.objects.create(tweet_id=tweet.id, address=choices[0]["text"])


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
