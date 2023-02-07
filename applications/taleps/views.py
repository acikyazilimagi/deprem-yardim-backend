from rest_framework.viewsets import ViewSet

from core.pagination import LocationPagination

from rest_framework.response import Response
import json

class TalepsViewSet(ViewSet):
    def list(self, request):
        return Response(
            data=json.loads({
                "Hello": "World"
            }),
            status=200
        )
    
    def retrieve(self, request, pk=None):
        return Response(
            data=json.loads({
                "Hello": "World"
            }),
            status=200
        ) 