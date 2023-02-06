from rest_framework.viewsets import ModelViewSet
from tweets.models import Location
from tweets.serializers import LocationSerializer


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.select_related("address", "address__tweet").filter(is_approved=True)
    serializer_class = LocationSerializer
    http_method_names = ["options", "head", "get"]
