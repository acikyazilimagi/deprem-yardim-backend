# Standard Library
from typing import Dict, List, Union

# Rest Framework
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# Applications
from feeds.models import Entry, Location


class BaseEntrySerializer(serializers.ModelSerializer):
    def validate(self, attrs: Dict[str, Union[str, float, bool]]):
        if attrs.get("is_geolocated"):
            location = attrs.get("location", None)
            if not location:
                raise ValidationError({"detail": ".location parameter invalid. E.g. [36.2039319, 36.1571015] "})
            if len(location) != 2:
                raise ValidationError({"detail": ".location parameter invalid. E.g. [36.2039319, 36.1571015] "})
            for loc in location:
                if type(loc) != float:
                    raise ValidationError({"detail": ".location parameter invalid. E.g. [36.2039319, 36.1571015] "})
        return attrs


class BulkEntrySerializer(BaseEntrySerializer):
    class Meta:
        model = Entry
        fields = ["full_text", "channel", "is_resolved", "is_geolocated", "location", "extra_parameters"]


class EntrySerializer(BaseEntrySerializer):
    def create(self, validated_data: Dict[str, Union[str, bool]]):
        # Applications
        from feeds.tasks import process_entry

        instance: Entry = super().create(validated_data=validated_data)
        process_entry.apply_async(kwargs={"entry_id": instance.id})
        return instance

    class Meta:
        model = Entry
        fields = [
            "id",
            "full_text",
            "timestamp",
            "channel",
            "is_resolved",
            "is_geolocated",
            "location",
            "extra_parameters",
        ]


class LocationLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "loc"]


class LocationSerializer(serializers.ModelSerializer):
    raw = EntrySerializer(source="entry")

    class Meta:
        model = Location
        fields = ["id", "formatted_address", "loc", "viewport", "raw"]


class LocationFilterParamSerializer(serializers.Serializer):
    """
    Filter by query param: timestamp
    """

    timestamp__gte = serializers.DateTimeField(required=False)
    timestamp__lte = serializers.DateTimeField(required=False)
