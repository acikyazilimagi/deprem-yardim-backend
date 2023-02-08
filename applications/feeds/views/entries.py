from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.authentication import AfetHaritaAuthentication
from rest_framework.authentication import BasicAuthentication, SessionAuthentication


from feeds.models import Entry
from feeds.serializers import EntrySerializer
from feeds.tasks import write_bulk_entries


class EntryViewSet(ModelViewSet):
    authentication_classes = [
        AfetHaritaAuthentication,
        BasicAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [IsAuthenticated]
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    http_method_names = ["options", "head", "post", "get"]


class BulkEntryView(APIView):
    write_task = write_bulk_entries
    permission_classes = [IsAuthenticated]
    authentication_classes = [
        AfetHaritaAuthentication,
        BasicAuthentication,
        SessionAuthentication,
    ]

    def post(self, request: Request) -> Response:
        self.write_task.apply_async(kwargs={"entries": request.data})
        return Response({"detail": "successful"})
