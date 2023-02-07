from rest_framework import serializers
from feeds.models import Entry


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ["full_text", "channel", "is_resolved", "extra_parameters"]
