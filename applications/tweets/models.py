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
    media = models.CharField(max_length=512, null=True)

    class Meta:
        ordering = ["-id"]


class Address(models.Model):
    tweet = models.ForeignKey("tweets.Tweet", on_delete=models.CASCADE, null=True)
    instagram_post = models.ForeignKey("instagram.InstagramPost", on_delete=models.CASCADE, null=True)
    address = models.TextField()
    city = models.CharField(max_length=255, null=True, blank=True)
    distinct = models.CharField(max_length=255, null=True, blank=True)
    neighbourhood = models.CharField(max_length=255, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    no = models.CharField(max_length=255, null=True, blank=True)
    name_surname = models.CharField(max_length=255, null=True, blank=True)
    tel = models.CharField(max_length=255, null=True, blank=True)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-id"]


class Location(models.Model):
    address = models.ForeignKey("tweets.Address", on_delete=models.CASCADE)
    formatted_address = models.TextField(null=True, blank=True)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    northeast_lat = models.FloatField(default=0.0)
    northeast_lng = models.FloatField(default=0.0)
    southwest_lat = models.FloatField(default=0.0)
    southwest_lng = models.FloatField(default=0.0)
    is_approved = models.BooleanField(default=False)

    @property
    def loc(self):
        return [self.latitude, self.longitude]

    @property
    def viewport(self):
        return {
            "northeast": {"lat": self.northeast_lat, "lng": self.northeast_lng},
            "southwest": {"lat": self.southwest_lat, "lng": self.southwest_lng},
        }

    class Meta:
        ordering = ["-id"]
