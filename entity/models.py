from django.db import models
from django.contrib.auth import get_user_model
from agent.models import Agent
from entity.utils import EntityTypesChoices

# Create your models here.
User = get_user_model()


class EntityTypes(models.Model):
    '''
    Model to define entities assoicated with an Agent
    '''
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True,
                                   on_delete=models.SET_NULL, related_name="agent_entityType_added_by")
    modified_by = models.ForeignKey(User, null=True,
                                    on_delete=models.SET_NULL, related_name="agent_entityType_modified_by")
    agent = models.ForeignKey(Agent, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True,)
    displayName = models.CharField(max_length=500, unique=True,)
    type = models.IntegerField(choices=EntityTypesChoices.choices(), default=EntityTypesChoices.DEFAULT)
    description = models.TextField('Entity Type description', blank=True, null=True)

    class Meta:
        verbose_name = "Entity Types"
        verbose_name_plural = "Entity Types"
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return f'{self.pk} - {self.name}'


class Entity(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True,
                                   on_delete=models.SET_NULL, related_name="agent_entity_added_by")
    modified_by = models.ForeignKey(User, null=True,
                                    on_delete=models.SET_NULL, related_name="agent_entity_modified_by")
    agent = models.ForeignKey(Agent, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True,)
    displayName = models.CharField(max_length=500, unique=True,)
    description = models.TextField('Entity Type description', blank=True, null=True)
    synonyms = models.TextField('Entity synonyms', blank=True, null=True)
    exclude = models.BooleanField(default=False)
    type = models.ManyToManyField(EntityTypes, related_name="entity_type")

    class Meta:
        verbose_name = "Entity"
        verbose_name_plural = "Entities"
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return f'{self.pk} - {self.name}'
