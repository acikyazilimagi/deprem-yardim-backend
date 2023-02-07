from tweets.models import Tweet
from tweets.helpers import bulk_ask_to_zekai
from trquake.celery import app
import pandas as pd
import snscrape.modules.twitter as sntwitter
import itertools
import datetime
from pytz import timezone


@app.task
def collect_tweets():
    data = []
    turkey = timezone("Europe/Istanbul")
    since_time = int(
        (
            datetime.datetime.now().replace(second=0, microsecond=0)
            - datetime.timedelta(minutes=7)
        ).timestamp()
    )

    query = f"""("1.kat" OR "2.kat" OR "3.kat" OR "4.kat" OR "5.kat" OR "6.kat" OR "7.kat" OR "8.kat" OR "9.kat" OR "10.kat" OR "11.kat") OR ("birincikat" OR "ikincikat" OR "üçüncükat" OR "dördüncükat" OR "beşincikat" OR "altıncıkat" OR "yedincikat" OR "sekizincikat" OR "dokuzuncukat" OR "onuncukat" OR "onbirincikat") OR ("bina" OR "apartman" OR "apt" OR "mahalle" OR "mahallesi" OR "bulvar" OR "sokak" OR "bulvarı" OR "göçük altında" OR "daire" OR "afad" OR "sk" OR "no:") lang:tr since_time:{since_time}"""
    df = pd.DataFrame(
        itertools.islice(
            sntwitter.TwitterSearchScraper(f"{query}").get_items(), 9999999
        )
    )
    df["date"] = df.date.apply(
        lambda x: pd.to_datetime(str(pd.to_datetime(x).astimezone(turkey))[:-6])
    )
    for ind in df.index:
        user_id = df["user"][ind]["id"]
        screen_name = df["user"][ind]["displayname"]
        name = df["user"][ind]["username"]
        tweet_id = df["id"][ind]
        created_at = df["date"][ind]
        full_text = df["rawContent"][ind]
        hashtags = [i for i in df["hashtags"]][ind]
        user_account_created_at = df['user'][ind]['created']
        try:
            media = df['media'][ind][0]['previewUrl']
        except (KeyError, TypeError):
            media = None
        
        data.append(
            Tweet(
                user_id=user_id,
                screen_name=screen_name,
                name=name,
                tweet_id=tweet_id,
                created_at=created_at,
                full_text=full_text,
                hashtags=hashtags,
                user_account_created_at=user_account_created_at,
                media=media
            )
        )
    created_tweets = Tweet.objects.bulk_create(data, ignore_conflicts=True)
    bulk_ask_to_zekai(tweet_data=created_tweets)
