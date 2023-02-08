from rest_framework import serializers
from feeds.models import Entry, Location
from typing import Dict, Union


class BulkEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ["full_text", "channel", "is_resolved", "extra_parameters"]


class EntrySerializer(serializers.ModelSerializer):
    def create(self, validated_data: Dict[str, Union[str, bool]]):
        from feeds.tasks import process_entry

        instance: Entry = super().create(validated_data=validated_data)
        process_entry.apply_async(kwargs={"entry_id": instance.id})
        return instance

    class Meta:
        model = Entry
        fields = ["id", "full_text", "timestamp", "channel", "is_resolved", "extra_parameters"]


class AreaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "loc"]


class LocationSerializer(serializers.ModelSerializer):
    raw = EntrySerializer(source="entry")

    class Meta:
        model = Location
        fields = ["id", "formatted_address", "loc", "viewport", "raw"]
