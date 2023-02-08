from rest_framework.viewsets import ModelViewSet
from feeds.serializers import LocationSerializer
from core.pagination import LocationPagination
from feeds.models import Location
from feeds.filters import LocationFilterBackend


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.select_related("entry").all()
    serializer_class = LocationSerializer
    http_method_names = ["options", "head", "get"]
    pagination_class = LocationPagination
    filter_backends = [LocationFilterBackend]
