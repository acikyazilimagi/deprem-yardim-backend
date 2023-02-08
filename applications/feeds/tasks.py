# Standard Library
from typing import Dict, List, Union

# Applications
from core.address_api import AddressAPI
from feeds.models import Entry, Location
from feeds.serializers import BulkEntrySerializer

# Backend
from trquake.celery import app


@app.task
def process_entry(entry_id: int):
    address_api = AddressAPI()
    entry = Entry.objects.get(id=entry_id)
    address_text = entry.full_text
    if not entry.is_resolved and not entry.is_geolocated:
        regex_response = address_api.regex_api_request(entry.full_text)
        if regex_response["ws"] < 0.71:
            # ask to openai
            return
        address_text = regex_response["address"]

    if not entry.is_geolocated:
        geolocation = address_api.trendyol_bff_api_request(address_text)
        if geolocation.get("is_resolved", False):
            entry.is_resolved = True
            entry.save()
            Location.objects.create(
                entry=entry,
                latitude=geolocation["latitude"],
                longitude=geolocation["longitude"],
                northeast_lat=geolocation["northeast_lat"],
                northeast_lng=geolocation["northeast_lng"],
                southwest_lat=geolocation["southwest_lat"],
                southwest_lng=geolocation["southwest_lng"],
                formatted_address=geolocation["formatted_address"],
            )
    else:
        Location.objects.create(entry=entry, latitude=entry.location[0], longitude=entry.location[1])


@app.task
def write_bulk_entries(entries: List[Dict[str, Union[str, bool]]]):
    for entry_data in entries:
        serializer = BulkEntrySerializer(data=entry_data)
        if serializer.is_valid():
            entry: Entry = serializer.save()
            process_entry(entry_id=entry.id)
