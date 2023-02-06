from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
import logging


logger = logging.getLogger(__name__)


class HealthCheckView(APIView):
    def get(self, request: Request) -> Response:
        logger.debug(request.get_host())
        return Response(data={"status": "ok"})
