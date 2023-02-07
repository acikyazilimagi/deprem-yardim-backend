from rest_framework import serializers
from tweets.models import Location, Tweet, Address
from instagram.models import InstagramPost


class InstagramPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramPost
        fields = ["full_text", "post_id", "user_id", "name", "screen_name"]
