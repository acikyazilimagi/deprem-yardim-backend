# Django Stuff
from django.db import models
from django.contrib.postgres.fields import ArrayField


class Entry(models.Model):
    CHANNEL_CHOICES = (
        ("twitter", "twitter"),
        ("telegram", "telegram"),
        ("twitch", "twitch"),
        ("discord", "discord"),
        ("depremyardim", "depremyardim"),
        ("manual", "manual"),
    )

    full_text = models.TextField()
    location = ArrayField(base_field=models.FloatField(default=0.0), null=True)
    is_resolved = models.BooleanField(default=False)
    is_geolocated = models.BooleanField(default=False)
    channel = models.CharField(max_length=255, choices=CHANNEL_CHOICES)
    extra_parameters = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ["-id"]


class Location(models.Model):
    entry = models.ForeignKey(
        "feeds.Entry", on_delete=models.CASCADE, related_query_name="entry", related_name="entries"
    )
    formatted_address = models.TextField(null=True, blank=True)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    northeast_lat = models.FloatField(default=0.0)
    northeast_lng = models.FloatField(default=0.0)
    southwest_lat = models.FloatField(default=0.0)
    southwest_lng = models.FloatField(default=0.0)

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
