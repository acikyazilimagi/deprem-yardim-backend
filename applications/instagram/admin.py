from django.contrib import admin
from instagram.models import Hashtag, InstagramPost, InstagramSession


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
