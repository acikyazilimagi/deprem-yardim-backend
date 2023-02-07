from django.http import HttpResponse
import json


class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/core/health/':
            return HttpResponse(json.dumps({"status": "ok"}))
        return self.get_response(request)
