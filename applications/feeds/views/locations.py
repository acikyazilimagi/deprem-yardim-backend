# Rest Framework
from rest_framework.viewsets import ModelViewSet

# Applications
from feeds.models import Location
from core.pagination import LocationPagination
from feeds.filters import TimestampFilterBackend
from feeds.serializers import LocationSerializer


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.select_related("entry").all()
    serializer_class = LocationSerializer
    http_method_names = ["options", "head", "get"]
    pagination_class = LocationPagination
    filter_backends = [TimestampFilterBackend]
