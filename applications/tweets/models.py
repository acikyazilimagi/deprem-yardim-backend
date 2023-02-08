from django.db import models


class DepremAddress(models.Model):
    full_text = models.TextField()
    tweet_id = models.CharField(max_length=255)
    screen_name = models.CharField(max_length=512)
    created_at = models.DateTimeField(null=True, blank=True)
    geo_link = models.CharField(max_length=512, default="")
    intent_result = models.TextField(null=True)
    is_done = models.BooleanField(default=False)

    class Meta:
        ordering = ["-id"]
