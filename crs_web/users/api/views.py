import json
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import permissions
from crs_web.users.models import UserProfile
from .serializers import UserSerializer, GroupSerializer, UserProfileSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-date_joined')
    lookup_field = "pk"
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class GroupViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserProfileViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    lookup_field = "pk"

    def post(self, request):
        data = request.data
        print(data['id'])
        id = data['id']
        try:
            instance = UserProfile.objects.get(id=id)
            instance.first_name = data['first_name']
            instance.last_name = data['last_name']
            instance.gender = data['gender']
            instance.movie_pref_1 = data['movie_pref_1']
            instance.movie_pref_2 = data['movie_pref_2']
            instance.movie_pref_3 = data['movie_pref_3']
            instance.save()
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileByUserViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        user_id = self.request.query_params['user_id']
        return UserProfile.objects.filter(user_id=user_id)


class UserProfileData(APIView):
    def get(self, request):
        user_profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(user_profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        user_profiles = UserProfile.objects.all()
        return user_profiles

    def post(self, request):
        data = request.data
        print(data['id'])
        id = data['id']
        try:
            instance = UserProfile.objects.get(id=id)
            instance.first_name = data['first_name']
            instance.last_name = data['last_name']
            instance.gender = data['gender']
            instance.movie_pref_1 = data['movie_pref_1']
            instance.movie_pref_2 = data['movie_pref_2']
            instance.movie_pref_3 = data['movie_pref_3']
            instance.save()
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
