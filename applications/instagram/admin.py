from django.contrib import admin
from instagram.models import (
    Hashtag,
    InstagramPost,
    InstagramSession,
    InstagramPostToFollow,
    InstagramComment,
)


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at", "updated_at"]
    search_fields = ["name"]

    class Meta:
        model = Hashtag


@admin.register(InstagramSession)
class InstagramSessionAdmin(admin.ModelAdmin):
    list_display = ["username", "is_valid", "created_at", "updated_at"]
    search_fields = ["username"]

    class Meta:
        model = InstagramSession


@admin.register(InstagramPost)
class InstagramPostAdmin(admin.ModelAdmin):
    list_display = ["post_id", "screen_name", "created_at"]
    search_fields = ["post_id", "screen_name", "created_at"]

    class Meta:
        model = InstagramPost


@admin.register(InstagramPostToFollow)
class InstagramPostToFollowAdmin(admin.ModelAdmin):
    list_display = ["url", "created_at", "updated_at"]
    search_fields = ["url"]

    class Meta:
        model = InstagramPostToFollow


@admin.register(InstagramComment)
class InstagramCommentAdmin(admin.ModelAdmin):
    list_display = ["comment_id", "screen_name", "followed_post", "created_at"]
    search_fields = ["comment_id", "screen_name", "followed_post", "created_at"]

    class Meta:
        model = InstagramComment
