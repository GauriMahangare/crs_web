from django.db import models
from django.contrib.auth import get_user_model

from agent.models import Agent
# Create your models here.
from .utils import EventActionTypesChoices
# Create your models here.
User = get_user_model()


class Event(models.Model):
    '''
    Model to define Events assoicated with an Intent
    '''
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True,
                                   on_delete=models.SET_NULL, related_name="agent_event_added_by")
    modified_by = models.ForeignKey(User, null=True,
                                    on_delete=models.SET_NULL, related_name="agent_event_modified_by")
    agent = models.ForeignKey(Agent, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255, unique=True,)
    displayName = models.CharField(max_length=500, unique=True,)
    description = models.TextField('Event description', blank=True, null=True)
    trigger_condition = models.TextField('Event condition', blank=True, null=True)

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return f'{self.pk} - {self.name}'


class Intent(models.Model):
    '''
    Model to define Intents assoicated with an Agent
    '''
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True,
                                   on_delete=models.SET_NULL, related_name="agent_intent_added_by")
    modified_by = models.ForeignKey(User, null=True,
                                    on_delete=models.SET_NULL, related_name="agent_intent_modified_by")
    agent = models.ForeignKey(Agent, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255, unique=True,)
    displayName = models.CharField(max_length=500, unique=True,)
    description = models.TextField('Intent description', blank=True, null=True)

    class Meta:
        verbose_name = "Intent"
        verbose_name_plural = "Intents"
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return f'{self.pk} - {self.name}'


class IntentExample(models.Model):
    '''
    Model to define Intent Examples for NLU
    '''
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True,
                                   on_delete=models.SET_NULL, related_name="agent_intentexample_added_by")
    modified_by = models.ForeignKey(User, null=True,
                                    on_delete=models.SET_NULL, related_name="agent_intentexample_modified_by")
    intent = models.ForeignKey(Intent, null=True, on_delete=models.SET_NULL, related_name='intent')
    example_text = models.TextField('NLU keywords', blank=True, null=True)

    class Meta:
        verbose_name = "Intent Example"
        verbose_name_plural = "Intent Examples"
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return f'{self.pk} - {self.example_text}'


class IntentResponseEvent(models.Model):
    '''
    Model to define Intent Response
    '''
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True,
                                   on_delete=models.SET_NULL, related_name="agent_intentresponse_added_by")
    modified_by = models.ForeignKey(User, null=True,
                                    on_delete=models.SET_NULL, related_name="agent_intentresponse_modified_by")
    intent = models.ForeignKey(Intent, null=True, on_delete=models.SET_NULL)
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Intent Response Event"
        verbose_name_plural = "Intent Response Events"
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return f'{self.pk} - {self.intent.name} - {self.event.name}'


class IntentEventAction(models.Model):
    '''
    Model to define Events assoicated with an Intent
    '''
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True,
                                   on_delete=models.SET_NULL, related_name="agent_eventAction_added_by")
    modified_by = models.ForeignKey(User, null=True,
                                    on_delete=models.SET_NULL, related_name="agent_eventAction_modified_by")
    agent = models.ForeignKey(Agent, null=True, on_delete=models.SET_NULL)
    intentResponseEvent = models.ForeignKey(IntentResponseEvent, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255, unique=True,)
    displayName = models.CharField(max_length=500, unique=True,)
    description = models.TextField('Event Action description', blank=True, null=True)
    response_type = models.IntegerField(choices=EventActionTypesChoices.choices(),
                                        default=EventActionTypesChoices.TEXT)

    class Meta:
        verbose_name = "Intent Event Action"
        verbose_name_plural = "Intent Event Actions"
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return f'{self.pk} - {self.name}'


class ResponseText(models.Model):
    '''
    Model to define text responses for an intent
    '''
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True,
                                   on_delete=models.SET_NULL, related_name="intent_responseText_added_by")
    modified_by = models.ForeignKey(User, null=True,
                                    on_delete=models.SET_NULL, related_name="intent_responseText_modified_by")
    agent = models.ForeignKey(Agent, null=True, on_delete=models.SET_NULL)
    intent_event_action = models.ForeignKey(IntentEventAction, null=True, on_delete=models.SET_NULL)
    response_text = models.TextField('Intent response', blank=True, null=True)

    class Meta:
        verbose_name = "Intent Response Text"
        verbose_name_plural = "Intent Response Texts"
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return f'{self.pk} - {self.response_text}'
