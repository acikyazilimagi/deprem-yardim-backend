from rest_framework.viewsets import ModelViewSet

from core.pagination import LocationPagination
from tweets.models import Location
from tweets.serializers import LocationSerializer


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.select_related("address", "address__tweet").all()
    serializer_class = LocationSerializer
    http_method_names = ["options", "head", "get"]
    pagination_class = LocationPagination
