from rest_framework.routers import DefaultRouter
from tweets.views import LocationViewSet, AreaViewSet

router = DefaultRouter(trailing_slash=False)
router.register("locations", LocationViewSet, basename="list-locations")
router.register("areas", AreaViewSet, basename="list-area")

urlpatterns = router.urls
