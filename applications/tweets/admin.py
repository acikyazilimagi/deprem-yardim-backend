from django.contrib import admin
from tweets.models import DepremAddress


@admin.register(DepremAddress)
class DepremAddressAdmin(admin.ModelAdmin):
    list_display = ["full_text", "tweet_id", "screen_name", "created_at"]

    class Meta:
        model = DepremAddress
