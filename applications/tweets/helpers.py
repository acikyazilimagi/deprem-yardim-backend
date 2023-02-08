import pandas as pd
from pytz import timezone
import itertools
import snscrape.modules.twitter as sntwitter


def fetch_tweets(query: str):
    turkey = timezone("Europe/Istanbul")

    df = pd.DataFrame(
        itertools.islice(
            sntwitter.TwitterSearchScraper(f"{query}").get_items(), 9999999
        )
    )
    try:
        df["date"] = df.date.apply(
            lambda x: pd.to_datetime(str(pd.to_datetime(x).astimezone(turkey))[:-6])
        )
    except AttributeError:
        return []

    for ind in df.index:
        links = df["links"][ind][0]["url"] if df["links"][ind] else ""
        user_id = df["user"][ind]["id"]
        screen_name = df["user"][ind]["displayname"]
        name = df["user"][ind]["username"]
        tweet_id = df["id"][ind]
        created_at = df["date"][ind]
        full_text = df["rawContent"][ind]
        hashtags = [i for i in df["hashtags"]][ind]
        user_account_created_at = df["user"][ind]["created"]
        try:
            media = df["media"][ind][0]["previewUrl"]
        except (KeyError, TypeError):
            media = None

        yield {
            "full_text": str(full_text),
            "user_id": str(user_id),
            "screen_name": str(screen_name),
            "name": str(name),
            "tweet_id": str(tweet_id),
            "created_at": str(created_at),
            "hashtags": str(hashtags),
            "user_account_created_at": str(user_account_created_at),
            "media": str(media),
            "links": links,
        }
