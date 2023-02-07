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
