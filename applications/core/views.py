from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response


class HealthCheckView(APIView):
    def get(self, request: Request) -> Response:
        print(request.get_host())
        return Response(data={"status": "ok"})
