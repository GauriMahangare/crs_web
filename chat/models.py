import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
# Create your models here.
User = get_user_model()

# User = settings.AUTH_USER_MODEL


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField()
    sent_by = models.CharField(max_length=255, blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True,
                                   on_delete=models.SET_NULL, related_name="message_added_by")

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ('created_at',)

    def __str__(self) -> str:
        return f'{self.sent_by}'


class Room(models.Model):
    roomid = models.CharField(max_length=255, blank=True, null=True)
    client = models.CharField(max_length=255, blank=True, null=True)
    agent = models.ForeignKey(User, null=True,
                              on_delete=models.SET_NULL, related_name="rooms")
    messages = models.ManyToManyField(Message, blank=True)
    url = models.URLField(
        "Website",
        blank=True,
        null=True,
    )

    class StatusChoices(models.TextChoices):
        WAITING = "Waiting", _("Waiting")
        ACTIVE = "Active", _("Active")
        CLOSED = "Closed", _("Closed")

    status = models.CharField(
        "Status",
        max_length=25,
        blank=True,
        choices=StatusChoices.choices,
        default=StatusChoices.WAITING,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return f'{self.client} - {self.roomid}'
