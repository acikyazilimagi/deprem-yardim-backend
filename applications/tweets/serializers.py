from rest_framework import serializers
from tweets.models import Location, Tweet, Address


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ["full_text", "tweet_id", "user_id", "name", "screen_name"]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["address", "city", "distinct", "neighbourhood", "street", "no", "name_surname", "tel"]


class LocationSerializer(serializers.ModelSerializer):
    raw = TweetSerializer(source="address.tweet")
    resolution = AddressSerializer(source="address")

    class Meta:
        model = Location
        fields = ["id", "formatted_address", "loc", "viewport", "raw", "resolution"]

