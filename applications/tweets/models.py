from django.db import models


class DepremAddress(models.Model):
    full_text = models.TextField()
    tweet_id = models.CharField(max_length=255)
    screen_name = models.CharField(max_length=512)
    created_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-id"]
