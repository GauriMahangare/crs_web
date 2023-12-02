import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from agent.models import Agent
from intent.models import Intent, IntentResponseEvent, IntentEventAction, ResponseText

# Create your models here.
User = get_user_model()

# User = settings.AUTH_USER_MODEL


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class StatusChoices(models.TextChoices):
        WAITING = "Waiting", _("Waiting")
        ACTIVE = "Active", _("Active")
        CLOSED = "Closed", _("Closed")

    status = models.CharField(
        "Conversation Status",
        max_length=25,
        blank=True,
        choices=StatusChoices.choices,
        default=StatusChoices.WAITING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True,
                                   on_delete=models.SET_NULL, related_name="conversation_added_by")
    url = models.URLField(
        "chat session url",
        blank=True,
        null=True,
    )
    with_agent = models.ForeignKey(Agent, null=True, on_delete=models.SET_NULL,)
    context_data = models.JSONField(null=True)

    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return f'{self.created_by} - {self.id}'


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField()

    class SentByChoices(models.TextChoices):
        HUMAN = "Human", _("Human")
        AI = "AI", _("AI")
        SYSTEM = "System", _("System")

    sent_by = models.CharField("Sent By", max_length=255, blank=True, null=False,
                               choices=SentByChoices.choices,
                               default=SentByChoices.SYSTEM,
                               )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True,
                                   on_delete=models.SET_NULL, related_name="message_added_by")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="message_modified_by"
    )
    session_id = models.CharField(max_length=255, blank=True, null=False)
    context_data = models.JSONField(null=True)
    conversationId = models.ForeignKey(
        Conversation, null=True, on_delete=models.CASCADE, related_name="conversation_id"
    )

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ('created_at',)

    def __str__(self) -> str:
        return f'{self.sent_by}'


class MessageFlow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True,
                                   on_delete=models.SET_NULL, related_name="messageFlow_added_by")
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="messageFlow_modified_by"
    )
    message = models.ForeignKey(Message, null=True, on_delete=models.CASCADE)
    intent = models.ForeignKey(Intent, null=True, on_delete=models.SET_NULL)
    intentResponseEvent = models.ForeignKey(IntentResponseEvent, null=True, on_delete=models.SET_NULL)
    IntentEventAction = models.ForeignKey(IntentEventAction, null=True, on_delete=models.SET_NULL)
    ResponseText = models.ForeignKey(ResponseText, null=True, on_delete=models.SET_NULL)
    entity_data = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "Message Flow"
        verbose_name_plural = "Message Flow"
        ordering = ('created_at',)

    def __str__(self) -> str:
        return f'{self.id}'
