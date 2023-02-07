from rest_framework.routers import DefaultRouter
from taleps.views import TalepsViewSet


router = DefaultRouter(trailing_slash=False)
router.register("locations", TalepsViewSet, basename="")

urlpatterns = router.urls
