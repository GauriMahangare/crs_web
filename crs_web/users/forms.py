from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.forms import EmailField
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import UserProfile

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User
        field_classes = {"email": EmailField}


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """


class CustomSignupForm(SignupForm):
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
    first_name = forms.CharField(required=True)
    movie_pref_1 = forms.ChoiceField(choices=MOVIE_CATEGOES_CHOICES, label='Movie Genre Pref 1')
    movie_pref_2 = forms.ChoiceField(choices=MOVIE_CATEGOES_CHOICES, label='Movie Genre Pref 2')
    movie_pref_3 = forms.ChoiceField(choices=MOVIE_CATEGOES_CHOICES, label='Movie Genre Pref 3')

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        # Add your custom validation logic here
        return first_name

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)

        # Map form fields to UserProfile model
        UserProfile.objects.create(
            user=user,
            # Add any other fields you need
            first_name=self.cleaned_data['first_name'],
            movie_pref_1=self.cleaned_data['movie_pref_1'],
            movie_pref_2=self.cleaned_data['movie_pref_2'],
            movie_pref_3=self.cleaned_data['movie_pref_3'],
        )

        return user
