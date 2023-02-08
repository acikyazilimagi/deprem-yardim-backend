from trquake.celery import app
import datetime
from tweets.models import DepremAddress
from feeds.models import Entry
from typing import List
import json
from feeds.tasks import process_entry
from tweets.helpers import fetch_tweets


@app.task
def collect_tweets():
    data = []
    since_time = int(
        (
            datetime.datetime.now().replace(second=0, microsecond=0)
            - datetime.timedelta(minutes=7)
        ).timestamp()
    )
    query = f"""("1.kat" OR "2.kat" OR "3.kat" OR "4.kat" OR "5.kat" OR "6.kat" OR "7.kat" OR "8.kat" OR "9.kat" OR "10.kat" OR "11.kat") OR ("birincikat" OR "ikincikat" OR "üçüncükat" OR "dördüncükat" OR "beşincikat" OR "altıncıkat" OR "yedincikat" OR "sekizincikat" OR "dokuzuncukat" OR "onuncukat" OR "onbirincikat") OR ("bina" OR "apartman" OR "apt" OR "mahalle" OR "mahallesi" OR "bulvar" OR "sokak" OR "bulvarı" OR "göçük altında" OR "daire" OR "afad" OR "sk" OR "no:") lang:tr since_time:{since_time}"""
    for tweet in fetch_tweets(query=query):
        data.append(
            Entry(
                full_text=tweet["full_text"],
                is_resolved=False,
                channel="twitter",
                extra_parameters=json.dumps(
                    {
                        "user_id": tweet["user_id"],
                        "screen_name": tweet["screen_name"],
                        "name": tweet["name"],
                        "tweet_id": tweet["tweet_id"],
                        "created_at": tweet["created_at"],
                        "hashtags": tweet["hashtags"],
                        "user_account_created_at": tweet["user_account_created_at"],
                        "media": tweet["media"],
                    }
                ),
            )
        )
    created_tweets: List[Entry] = Entry.objects.bulk_create(data)
    for entry in created_tweets:
        process_entry.apply_async(kwargs={"entry_id": entry.id})


@app.task
def collect_deprem_address_tweets():
    data = []
    since_time = int(
        (
            datetime.datetime.now().replace(second=0, microsecond=0)
            - datetime.timedelta(minutes=7)
        ).timestamp()
    )
    query = f""""#depremadres" since_time:{since_time}"""
    for tweet in fetch_tweets(query=query):
        data.append(
            DepremAddress(
                full_text=tweet["full_text"],
                tweet_id=tweet["tweet_id"],
                screen_name=tweet["screen_name"],
                created_at=tweet["created_at"],
                geo_link=tweet["links"],
            )
        )

    DepremAddress.objects.bulk_create(data)
