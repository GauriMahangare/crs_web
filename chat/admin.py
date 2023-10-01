from django.contrib import admin

# Register your models here.
from .models import Message, Conversation

# Register your models here.


class MessageAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"

    # to filter the resultes by users, content types and action flags
    list_filter = [
        "sent_by",
        "created_by",
        "conversationId",
        "session_id",
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        "sent_by",
        "created_by",
        "session_id",
        "conversationId",
    ]

    list_display = [
        "id",
        "body",
        "sent_by",
        "created_at",
        "created_by",
        "session_id",
        "context_data",
        "conversationId",
    ]


admin.site.register(Message, MessageAdmin)


class ConversationAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"

    # to filter the resultes by users, content types and action flags
    list_filter = [
        "created_by",
        "status",
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        "created_by",
        "created_at"
    ]

    list_display = [
        "id",
        "status",
        "created_at",
        "created_by",
        "url",
        "context_data",

    ]


admin.site.register(Conversation, ConversationAdmin)
