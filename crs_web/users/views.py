from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from .models import UserProfile
User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name", "email"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert self.request.user.is_authenticated  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        user = get_object_or_404(User, id=self.request.user.pk)
        return user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()
# ######
# User profile views
# ######


class UserProfileRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_profile_redirect_view = UserProfileRedirectView.as_view()


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    slug_field = "id"
    slug_url_kwarg = "id"
    template_name = "users/userprofile_form.html"


user_profile_detail_view = UserProfileDetailView.as_view()


class UserProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = UserProfile
    fields = ["first_name", "last_name", "gender", "movie_pref_1", "movie_pref_2", "movie_pref_3"]
    success_message = _("Information successfully updated")
    template_name = "users/userprofile_form.html"

    def get_success_url(self):
        print("in get_success_url")
        return reverse("users:detail", args=[self.request.user.pk])

    def get_object(self):
        user_profile = get_object_or_404(UserProfile, user_id=self.request.user)
        return user_profile


user_profile_update_view = UserProfileUpdateView.as_view()
