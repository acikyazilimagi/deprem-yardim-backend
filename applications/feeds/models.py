from django.db import models


class Entry(models.Model):
    CHANNEL_CHOICES = (
        ("twitter", "twitter"),
        ("telegram", "telegram"),
        ("twitch", "twitch"),
        ("discord", "discord"),
    )

    full_text = models.TextField()
    is_resolved = models.BooleanField(default=False)
    channel = models.CharField(max_length=255, choices=CHANNEL_CHOICES)
    extra_parameters = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ["-id"]


class Location(models.Model):
    entry = models.ForeignKey("feeds.Entry", on_delete=models.CASCADE)
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

