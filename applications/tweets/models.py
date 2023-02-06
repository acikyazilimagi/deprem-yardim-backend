from django.db import models
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
    media= models.CharField(max_length=512)

    class Meta:
        ordering = ["-id"]


class Address(models.Model):
    tweet = models.ForeignKey("tweets.Tweet", on_delete=models.CASCADE)
    address = models.TextField()

    class Meta:
        ordering = ["-id"]
