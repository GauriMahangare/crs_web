from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework import serializers

from entity.models import EntityTypes, Entity


class EntityTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityTypes
        fields = ["id", "agent", "name", 'displayName', 'created_at', 'created_by', 'type', 'description']


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ["id", "agent", "name", 'created_at', 'created_by',
                  'displayName', 'description', 'synonyms', 'exclude', 'type']
