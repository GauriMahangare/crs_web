from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework import serializers

from agent.models import Agent


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ["id", "name", 'description', 'created_at', 'created_by', ]
