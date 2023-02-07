from rest_framework.routers import DefaultRouter
from feeds.views import (
    EntryViewSet,
    BulkEntryView,
    LocationViewSet,
    AreaViewSet,
    AreasCountViewSet,
    CityByCityCountView,
)
from django.urls import path

router = DefaultRouter(trailing_slash=False)
router.register("locations", LocationViewSet, basename="list-locations")
router.register("entries", EntryViewSet, basename="create-entry")
router.register("areas/count", AreasCountViewSet, basename="count-area")
router.register("areas", AreaViewSet, basename="list-area")

urlpatterns = [
    path("entries/bulk", BulkEntryView.as_view()),
    path("cities", CityByCityCountView.as_view()),
] + router.urls
