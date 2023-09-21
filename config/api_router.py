from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from crs_web.users.api.views import UserViewSet, GroupViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("groups", GroupViewSet)

app_name = "api"
urlpatterns = router.urls
