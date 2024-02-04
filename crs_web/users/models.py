from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models
from crs_web.users.managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for CRS_WEB.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    MOVIE_CATEGOES_CHOICES = [('Documentary', 'Documentary'),
                              ('Animation', 'Animation'),
                              ('Comedy', 'Comedy'),
                              ('Short', 'Short'),
                              ('Romance', 'Romance'),
                              ('News', 'News'),
                              ('Drama', 'Drama'),
                              ('Fantasy', 'Fantasy'),
                              ('Horror', 'Horror'),
                              ('Biography', 'Biography'),
                              ('Music', 'Music'),
                              ('Crime', 'Crime'),
                              ('Family', 'Family'),
                              ('Adventure', 'Adventure'),
                              ('Action', 'Action'),
                              ('History', 'History'),
                              ('Mystery', 'Mystery'),
                              ('Musical', 'Musical'),
                              ('War', 'War'),
                              ('Sci-Fi', 'Sci-Fi'),
                              ('Western', 'Western'),
                              ('Thriller', 'Thriller'),
                              ('Sport', 'Sport'),
                              ('Film-Noir', 'Film-Noir'),
                              ('Talk-Show', 'Talk-Show'),
                              ('Game-Show', 'Game-Show'),
                              ('Adult', 'Adult'),
                              ('Reality-TV', 'Reality-TV'),
                              ]
    movie_pref_1 = CharField(max_length=60, choices=MOVIE_CATEGOES_CHOICES)
    movie_pref_2 = CharField(max_length=60, choices=MOVIE_CATEGOES_CHOICES)
    movie_pref_3 = CharField(max_length=60, choices=MOVIE_CATEGOES_CHOICES)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
