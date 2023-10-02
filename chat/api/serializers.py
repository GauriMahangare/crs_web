from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework import serializers

from chat.models import Message, Conversation


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "body", 'sent_by', 'created_at', 'created_by', 'conversationId',]


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ["id", "status", 'created_at', 'created_by',]
