from rest_framework.viewsets import ModelViewSet

from core.pagination import LocationPagination
from taleps.models import TalepLocation
from taleps.serializers import LocationSerializer

class TalepsViewSet(ModelViewSet):
    queryset = TalepLocation.objects.select_related("address").all()
    serializer_class = LocationSerializer
    http_method_names = ["options", "head", "get"]
    pagination_class = LocationPagination