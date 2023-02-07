from django.db import models
from core.models import CommonAddress, CommonLocation
from django.contrib.postgres.fields import ArrayField


class Tweet(models.Model):
    user_id = models.CharField(max_length=255)
    screen_name = models.CharField(max_length=512)
    name = models.CharField(max_length=255)
    verified = models.BooleanField(default=False)
    tweet_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(null=True, blank=True)
    full_text = models.TextField()
    hashtags = ArrayField(base_field=models.CharField(max_length=255), null=True)
    user_account_created_at = models.DateTimeField(null=True, blank=True)
    media = models.CharField(max_length=512, null=True)

    class Meta:
        ordering = ["-id"]


class Address(CommonAddress):
    tweet = models.ForeignKey("tweets.Tweet", on_delete=models.CASCADE)


class Location(CommonLocation):
    address = models.ForeignKey("tweets.Address", on_delete=models.CASCADE)
