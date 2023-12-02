from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets
from rest_framework import permissions

from intent.models import Event, IntentEventAction, IntentExample, Intent, IntentResponseEvent

from .serializers import EventSerializer, IntentExampleSerializer, IntentResponseEventSerializer, IntentSerializer, IntentEventActionSerializer

User = get_user_model()


class EventViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all().order_by('-created_at')
    lookup_field = "pk"
    permission_classes = [permissions.IsAuthenticated]


class IntentExampleViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = IntentExampleSerializer
    queryset = IntentExample.objects.all().order_by('-created_at')
    lookup_field = "pk"
    permission_classes = [permissions.IsAuthenticated]


class IntentViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Intent.objects.all().order_by('-created_at')
    serializer_class = IntentSerializer
    permission_classes = [permissions.IsAuthenticated]


class IntentResponseEventViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = IntentResponseEvent.objects.all().order_by('-created_at')
    serializer_class = IntentResponseEventSerializer
    permission_classes = [permissions.IsAuthenticated]


class IntentEventActionViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = IntentEventAction.objects.all().order_by('-created_at')
    serializer_class = IntentEventActionSerializer
    permission_classes = [permissions.IsAuthenticated]
