from rest_framework import serializers
from tweets.serializers import LocationSerializer
from taleps.models import Talep, TalepAddress, TalepLocation

class TalepSerializer(serializers.ModelSerializer):
    resolution = LocationSerializer(source="location")

    class Meta:
        model = Talep
        fields = ["id", "location", "source", "extra_info"]

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalepAddress
        fields = ["address", "city", "distinct", "neighbourhood", "street", "no", "name_surname", "tel"]


class LocationSerializer(serializers.ModelSerializer):
    resolution = AddressSerializer(source="address")

    class Meta:
        model = TalepLocation
        fields = ["id", "formatted_address", "loc", "viewport", "resolution"]