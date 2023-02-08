from django.db import models
from django.contrib.postgres.fields import ArrayField


class Hashtag(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.name}"


class InstagramSession(models.Model):
    is_valid = models.BooleanField(default=True)
    username = models.CharField(max_length=255)
    settings = models.JSONField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class InstagramPost(models.Model):
    user_id = models.CharField(max_length=255)
    screen_name = models.CharField(max_length=512)
    name = models.CharField(max_length=255)
    verified = models.BooleanField(default=False)
    post_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(null=True, blank=True)
    full_text = models.TextField()
    hashtags = ArrayField(base_field=models.CharField(max_length=255), null=True)
    user_account_created_at = models.DateTimeField(null=True, blank=True)
    media = models.CharField(max_length=512, null=True)

    class Meta:
        ordering = ["-id"]


class InstagramPostToFollow(models.Model):
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.url

    class Meta:
        ordering = ["-id"]
        verbose_name_plural = "Instagram posts to follow"


class InstagramComment(models.Model):
    followed_post = models.ForeignKey(
        "instagram.InstagramPostToFollow", on_delete=models.CASCADE
    )
    user_id = models.CharField(max_length=255)
    screen_name = models.CharField(max_length=512)
    name = models.CharField(max_length=255)
    post_id = models.CharField(max_length=255)
    comment_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(null=True, blank=True)
    full_text = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-id"]
