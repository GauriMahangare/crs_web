from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework import serializers

from intent.models import Event, Intent, IntentExample, IntentEventAction, IntentResponseEvent


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "agent", 'name', 'created_at', 'created_by', 'displayName', 'description', 'trigger_condition']


class IntentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intent
        fields = ["id", "agent", 'created_at', 'created_by', 'name',
                  'displayName', 'description', ]


class IntentExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntentExample
        intent = IntentSerializer(many=True, read_only=True)
        fields = ["id", 'created_at', 'created_by',
                  'intent', 'example_text']


class IntentResponseEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntentResponseEvent
        intent = IntentSerializer(many=True, read_only=True)
        event = EventSerializer(many=True, read_only=True)
        fields = ["id", 'created_at', 'created_by',
                  'intent', 'event']


class IntentEventActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntentEventAction
        intentResponseEvent = IntentResponseEventSerializer(many=True, read_only=True)
        fields = ["id", 'created_at', 'created_by',
                  'agent', 'intentResponseEvent', 'name', 'description', 'response_type']
