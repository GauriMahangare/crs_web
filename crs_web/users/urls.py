from django.urls import path

from crs_web.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    user_profile_update_view,
    user_profile_detail_view,
    user_profile_redirect_view,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
    path("profile/<int:pk>/", view=user_profile_detail_view, name="profile_detail"),
    path("profile/~update/", view=user_profile_update_view, name="profile_update"),
    path("profile/~redirect/", view=user_profile_redirect_view, name="profile_redirect"),
]
