from django.contrib import admin
from tweets.models import Address, Tweet, Location


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ["tweet_id", "screen_name", "created_at"]
    search_fields = ["tweet_id", "screen_name", "created_at"]

    class Meta:
        model = Tweet


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["get_tweet_id", "get_tweet_screen_name", "get_tweet_full_text", "address"]

    @admin.display(ordering="tweet__tweet_id", description="Tweet ID")
    def get_tweet_id(self, obj: Address):
        return obj.tweet.tweet_id

    @admin.display(ordering="tweet__tweet_screen_name", description="User Screen Name")
    def get_tweet_screen_name(self, obj: Address):
        return obj.tweet.screen_name

    @admin.display(ordering="tweet__tweet_full_text", description="Tweet")
    def get_tweet_full_text(self, obj: Address):
        return obj.tweet.full_text

    class Meta:
        model = Address


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["latitude", "longitude", "get_full_address", "formatted_address", "is_approved"]
    list_editable = ["is_approved"]
    list_filter = ["is_approved"]

    @admin.display(ordering="address__full_text", description="Full Address")
    def get_full_address(self, obj: Location):
        return obj.address.address

    class Meta:
        model = Location
