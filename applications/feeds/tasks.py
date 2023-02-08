# Standard Library
from typing import Dict, List, Union

# Applications
import requests, os, json
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
    if not entry.is_resolved:
        regex_response = address_api.regex_api_request(entry.full_text)
        if regex_response["ws"] < 0.71:
            # ask to openai
            return
        address_text = regex_response["address"]

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


@app.task
def write_bulk_entries(entries: List[Dict[str, Union[str, bool]]]):
    for entry_data in entries:
        serializer = BulkEntrySerializer(data=entry_data)
        if serializer.is_valid():
            entry: Entry = serializer.save()
            process_entry(entry_id=entry.id)


@app.task
def get_all_depremyardim():

    # 1. Tum datayi depremyardimdan get TODO: Multithread?
    data, new_data, i = [], {}, 1
    while len(new_data.get("data", [""])) > 0:
        req = requests.get(
            url = "https://depremyardim.com/api/list",
            params= {
                "X-AUTH-KEY": os.environ['DEPREM_YARDIM_AUTH_KEY'],
                "page": i,
                "per_page": "1000"
            }
        )
        new_data = json.loads(req.text)
        data.extend(new_data["data"]['data'])
        i+=1

    # TODO: Son kaldigimiz page'i kaydet ve her cron run da ordan devam et
    # 2. Databaseteki duplicatelari bul
    # TODO: extra_parameters le merge_conflict'leri bul ve yeni datadan sil

    # 3. Geri kalan datalar icin yeni entryler olustur
    for row in data:
        new_entry = Entry(
            full_text = json.dumps(row),
            is_resolved = False,
            channel = "depremyardim",
            extra_parameters = json.dumps(row)
        )
        new_entry.save()
        # TODO: Bu islem nasil calisiyor tam olarak
        new_location = AddressAPI.regex_api_request() #???
        if new_location.get("is_resolved", False):
            new_entry.is_resolved = True
            new_entry.save()
            Location.objects.create(
                entry=new_entry,
                latitude=new_location["latitude"],
                longitude=new_location["longitude"],
                northeast_lat=new_location["northeast_lat"],
                northeast_lng=new_location["northeast_lng"],
                southwest_lat=new_location["southwest_lat"],
                southwest_lng=new_location["southwest_lng"],
                formatted_address=new_location["formatted_address"],
            )