import tweepy
from django.conf import settings
from tweets.models import Tweet
from tweets.helpers import bulk_ask_to_zekai
from trquake.celery import app


@app.task
def collect_tweets():
    auth = tweepy.OAuth2BearerHandler(settings.TWITTER_BEARER_TOKEN)
    api = tweepy.API(auth)
    query = "#deprem"
    data = []

    for tweet in tweepy.Cursor(
        api.search_tweets, q=query, tweet_mode="extended", count=100
    ).items(1000):
        data.append(
            Tweet(
                user_id=tweet.user.id,
                screen_name=tweet.user.screen_name,
                name=tweet.user.name,
                verified=tweet.user.verified,
                tweet_id=tweet.id,
                created_at=tweet.created_at,
                full_text=tweet.full_text,
                hashtags=[h["text"] for h in tweet.entities["hashtags"]]
            )
        )
    created_tweets = Tweet.objects.bulk_create(data)
    bulk_ask_to_zekai(tweet_data=created_tweets)
