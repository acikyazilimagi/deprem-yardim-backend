from rest_framework.routers import DefaultRouter
from feeds.views.areas import AreaViewSet, AreaLiteViewSet, AreasCountViewSet, CityByCityCountView
from feeds.views.locations import LocationViewSet
from feeds.views.entries import EntryViewSet, BulkEntryView
from django.urls import path

router = DefaultRouter(trailing_slash=False)
router.register("locations", LocationViewSet, basename="list-locations")
router.register("entries", EntryViewSet, basename="create-entry")
router.register("areas", AreaViewSet, basename="list-area")
router.register("areas/count", AreasCountViewSet, basename="count-area")
router.register("areas-lite", AreaLiteViewSet, basename="list-area-lite")

urlpatterns = [
    path("entries/bulk", BulkEntryView.as_view()),
    path("cities", CityByCityCountView.as_view()),
] + router.urls
