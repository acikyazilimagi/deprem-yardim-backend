# Standard Library
import operator
from functools import reduce

# Django Stuff
from django.db.models import Q, Count

# Rest Framework
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

# Applications
from feeds.models import Location
from feeds.views.base import BaseAreaViewSet
from feeds.serializers import LocationSerializer, LocationLiteSerializer


class AreaViewSet(BaseAreaViewSet):
    serializer_class = LocationSerializer


class AreaLiteViewSet(BaseAreaViewSet):
    serializer_class = LocationLiteSerializer


class AreasCountViewSet(AreaViewSet):
    def list(self, request: Request, *args, **kwargs) -> Response:
        return Response({"count": self.get_queryset().count()})


class CityByCityCountView(APIView):
    CITY_LIST = {
        "Kahramanmaraş": ["Kahramanmaraş", "Kahramanmaras", "Elbistan", "Onikişubat"],
        "Gaziantep": ["Gaziantep"],
        "Hatay": ["Hatay", "Antakya", "İskenderun", "Iskenderun"],
        "Adana": ["Adana"],
        "Adıyaman": ["Adıyaman", "Adiyaman"],
        "Malatya": ["Malatya"],
        "Urfa": ["Urfa"],
        "Diyarbakır": ["Diyarbakır", "Diyarbakir", "Dıyarbakır", "Dıyarbakir"],
        "Kilis": ["Kilis", "Kılıs"],
        "Osmaniye": ["Osmaniye"],
        "Batman": ["Batman"],
        "Mersin": ["Mersin", "İçel", "Tarsus", "Icel"],
    }

    def get(self, request: Request) -> Response:
        kwargs = {}
        for city, keywords in self.CITY_LIST.items():
            kwargs[city] = Count(
                "id",
                filter=reduce(operator.or_, (Q(formatted_address__icontains=k) for k in keywords)),
            )

        return Response(data=Location.objects.aggregate(**kwargs))
