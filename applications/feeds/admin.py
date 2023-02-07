from django.contrib import admin
from feeds.models import Entry, Location


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ["id", "full_text", "channel", "is_resolved"]
    list_filter = ["is_resolved", "channel"]
    search_fields = ["full_text"]

    class Meta:
        model = Entry


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["formatted_address", "latitude", "longitude"]

    class Meta:
        model = Location
