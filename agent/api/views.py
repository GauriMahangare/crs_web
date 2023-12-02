from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets
from rest_framework import permissions

from agent.models import Agent

from .serializers import AgentSerializer

User = get_user_model()


class AgentViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = AgentSerializer
    queryset = Agent.objects.all().order_by('-created_at')
    lookup_field = "pk"
    permission_classes = [permissions.IsAuthenticated]
