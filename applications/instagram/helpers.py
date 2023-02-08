import logging

import requests
from core.helpers import analyze_with_zekai, login_to_zekai
from tweets.models import Address, Location
from instagram.models import InstagramPost, InstagramComment
from typing import List, Dict
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
import json

logger = logging.getLogger(__name__)


def ask_instagram_posts_to_zekai(headers: Dict[str, str], post: InstagramPost) -> None:
    ty_geolocation_url = "https://public-sdc.trendyol.com/discovery-web-websfxgeolocation-santral/geocode"
    submit_data = analyze_with_zekai(headers, post.full_text)
    if choices := submit_data.get("choices"):
        processed_address = json.loads(choices[0]["text"].strip())
        full_address = processed_address.get("address")
        # do we want to save this address when it doesn't even have address?
        if not full_address:
            return

        address = Address.objects.create(
            instagram_post_id=post.id,
            address=full_address,
            city=processed_address.get("city"),
            distinct=processed_address.get("distinct"),
            neighbourhood=processed_address.get("neighbourhood"),
            street=processed_address.get("street"),
            no=processed_address.get("no"),
            name_surname=processed_address.get("name_surname"),
            tel=processed_address.get("tel"),
        )

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
                formatted_address=geolocation["formatted_address"],
            )
            address.is_resolved = True
            address.save()


def ask_instagram_comments_to_zekai(
    headers: Dict[str, str], comment: InstagramComment
) -> None:
    ty_geolocation_url = "https://public-sdc.trendyol.com/discovery-web-websfxgeolocation-santral/geocode"
    submit_data = analyze_with_zekai(headers, comment.full_text)
    if choices := submit_data.get("choices"):
        processed_address = json.loads(choices[0]["text"].strip())
        full_address = processed_address.get("address")
        # do we want to save this address when it doesn't even have address?
        if not full_address:
            return

        address = Address.objects.create(
            instagram_comment_id=comment.id,
            address=full_address,
            city=processed_address.get("city"),
            distinct=processed_address.get("distinct"),
            neighbourhood=processed_address.get("neighbourhood"),
            street=processed_address.get("street"),
            no=processed_address.get("no"),
            name_surname=processed_address.get("name_surname"),
            tel=processed_address.get("tel"),
        )

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
                formatted_address=geolocation["formatted_address"],
            )
            address.is_resolved = True
            address.save()


def bulk_ask_instagram_posts_to_zekai(post_data: List[InstagramPost]):
    headers = login_to_zekai()
    thread_list: List[Future] = []
    thread_pool = ThreadPoolExecutor(max_workers=5)
    for post in post_data:
        thread = thread_pool.submit(
            ask_instagram_posts_to_zekai, headers=headers, post=post
        )
        thread_list.append(thread)

    for _ in as_completed(thread_list, timeout=4):
        pass


def bulk_ask_instagram_comments_to_zekai(comments_data: List[InstagramComment]):
    headers = login_to_zekai()
    thread_list: List[Future] = []
    thread_pool = ThreadPoolExecutor(max_workers=5)
    for comment in comments_data:
        thread = thread_pool.submit(
            ask_instagram_comments_to_zekai, headers=headers, comment=comment
        )
        thread_list.append(thread)

    for _ in as_completed(thread_list, timeout=4):
        pass


def extract_hashtags(text: str):
    hashtags = []
    for word in text.split():
        if word[0] == "#":
            hashtags.append(word[1:])
    return hashtags


def contains_query_word(text: str):
    query_words = [
        "1.kat",
        "2.kat",
        "3.kat",
        "4.kat",
        "5.kat",
        "6.kat",
        "7.kat",
        "8.kat",
        "9.kat",
        "10.kat",
        "11.kat",
        "birincikat",
        "ikincikat",
        "üçüncükat",
        "dördüncükat",
        "beşincikat",
        "altıncıkat",
        "yedincikat",
        "sekizincikat",
        "dokuzuncukat",
        "onuncukat",
        "onbirincikat",
        "bina",
        "apartman",
        "apt",
        "mahalle",
        "mahallesi",
        "bulvar",
        "sokak",
        "bulvarı",
        "göçük altında",
        "daire",
        "afad",
        "sk",
        "no:",
    ]
    for qw in query_words:
        if qw in text.lower():
            return True
    return False
