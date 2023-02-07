from trquake.celery import app
from typing import List, Dict, Union
from feeds.serializers import EntrySerializer


@app.task
def write_bulk_entries(entries: List[Dict[str, Union[str, bool]]]):
    for entry in entries:
        serializer = EntrySerializer(data=entry)
        if serializer.is_valid():
            serializer.save()
