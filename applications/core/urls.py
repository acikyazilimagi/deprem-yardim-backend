# Django Stuff
from django.urls import path

# Applications
from core.views import HealthCheckView

urlpatterns = [path("health/", HealthCheckView.as_view())]
