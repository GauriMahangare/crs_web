from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from crs_web.users.api.views import UserViewSet, GroupViewSet
from chat.api.views import MessageViewSet, ConversationViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("groups", GroupViewSet)
router.register("message", MessageViewSet)
router.register("conversation", ConversationViewSet)


app_name = "api"
urlpatterns = router.urls
