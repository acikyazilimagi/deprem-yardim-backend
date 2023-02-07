from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from feeds.models import Entry
from feeds.serializers import EntrySerializer
from feeds.tasks import write_bulk_entries


class EntryViewSet(ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    http_method_names = ["options", "head", "post", "get"]


class BulkEntryView(APIView):
    write_task = write_bulk_entries

    def post(self, request: Request) -> Response:
        self.write_task.apply_async(kwargs={"entries": request.data})
        return Response({"detail": "successful"})
