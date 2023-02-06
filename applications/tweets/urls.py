from rest_framework.routers import DefaultRouter
from tweets.views import LocationViewSet


router = DefaultRouter(trailing_slash=False)
router.register("locations", LocationViewSet)

urlpatterns = router.urls
