from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from crs_web.users.api.views import UserViewSet, GroupViewSet, UserProfileViewSet, UserProfileByUserViewSet, UserProfileData
from chat.api.views import MessageViewSet, ConversationViewSet
from agent.api.views import AgentViewSet
from entity.api.views import EntityTypesViewSet, EntityViewSet
from intent.api.views import IntentEventActionViewSet, EventViewSet, IntentExampleViewSet, IntentResponseEventViewSet, IntentViewSet


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("groups", GroupViewSet)
router.register("users-profile", UserProfileViewSet)
router.register("users-profile-by-user", UserProfileByUserViewSet, basename='users')
# router.register("users-profile", getUserProfileData, basename='user-profile')
# router.register("message", MessageViewSet)
# router.register("conversation", ConversationViewSet)
# router.register("agent", AgentViewSet)
# router.register("entityTypes", EntityTypesViewSet)
# router.register("entity", EntityViewSet)
# router.register("event", EventViewSet)
# router.register("intentExample", IntentExampleViewSet)
# router.register("intent", IntentViewSet)
# router.register("intentResponseEvent", IntentResponseEventViewSet)
# router.register("intentResponseEventAction", IntentEventActionViewSet)

urlpatterns = [
    path('user-prof-functional/', UserProfileData.as_view(), name='UserProfileData'),
]

app_name = "api"
urlpatterns += router.urls
