from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets
from rest_framework import permissions

from chat.models import Message, Conversation

from .serializers import MessageSerializer, ConversationSerializer

User = get_user_model()


class MessageViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all().order_by('-created_at')
    lookup_field = "pk"
    permission_classes = [permissions.IsAuthenticated]


class ConversationViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Conversation.objects.all().order_by('-created_at')
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
