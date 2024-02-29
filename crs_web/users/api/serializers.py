from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework import serializers

from crs_web.users.models import User as UserType
from crs_web.users.models import UserProfile

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name', 'gender',
                  'movie_pref_1', 'movie_pref_2', 'movie_pref_3', 'user_id']


class UserSerializer(serializers.ModelSerializer[UserType]):
    user_profile = UserProfileSerializer(source='UserProfile', read_only=True)

    class Meta:
        model = User
        fields = ["name", "url", 'email', 'groups', 'user_profile']

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
