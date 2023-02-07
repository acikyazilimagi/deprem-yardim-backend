from rest_framework.routers import DefaultRouter
from feeds.views import EntryViewSet, BulkEntryView
from django.urls import path

router = DefaultRouter(trailing_slash=False)
router.register("entries", EntryViewSet, basename="create-entry")

urlpatterns = [path("entries/bulk", BulkEntryView.as_view())] + router.urls
