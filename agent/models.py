import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Create your models here.
User = get_user_model()

# User = settings.AUTH_USER_MODEL


class Agent(models.Model):
    '''
    Model to define various chat agents
    '''
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True,
                                   on_delete=models.SET_NULL, related_name="agent_added_by")
    name = models.CharField(max_length=255, unique=True,)
    user = models.ForeignKey(User, null=True,
                             on_delete=models.SET_NULL, related_name="agent_user")
    description = models.TextField('agent description', blank=True, null=True)

    class Meta:
        verbose_name = "Agent"
        verbose_name_plural = "Agents"
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return f'{self.pk} - {self.name}'
