from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from core.pagination import LocationPagination, AreaPagination
from tweets.models import Location
from tweets.serializers import LocationSerializer


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.select_related("address", "address__tweet").all()
    serializer_class = LocationSerializer
    http_method_names = ["options", "head", "get"]
    pagination_class = LocationPagination

class AreaViewSet(GenericViewSet):
    serializer_class = LocationSerializer
    pagination_class = AreaPagination

    def get_queryset(self):
        return Location.objects.select_related("address", "address__tweet").all()

    def list(self, request: Request, *args, **kwargs) -> Response:
        ne_lat = self.request.query_params.get("ne_lat")
        ne_lng = self.request.query_params.get("ne_lng")
        sw_lat = self.request.query_params.get("sw_lat")
        sw_lng = self.request.query_params.get("sw_lng")

        if not ne_lat:
            return Response("Please provide ne_lat", status=status.HTTP_400_BAD_REQUEST)
        if not ne_lng:
            return Response("Please provide ne_lng", status=status.HTTP_400_BAD_REQUEST)
        if not sw_lat:
            return Response("Please provide sw_lat", status=status.HTTP_400_BAD_REQUEST)
        if not sw_lng:
            return Response("Please provide sw_lng", status=status.HTTP_400_BAD_REQUEST)
        try:
            ne_lat = float(ne_lat)
            ne_lng = float(ne_lng)
            sw_lat = float(sw_lat)
            sw_lng = float(sw_lng)
        except ValueError:
            return Response("Please provide float value.")

        self.queryset = self.get_queryset()

        self.queryset = self.queryset.filter(
            northeast_lat__lte=ne_lat,
            northeast_lng__gte=ne_lng,
            southwest_lat__lte=sw_lat,
            southwest_lng__gte=sw_lng
        )

        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
