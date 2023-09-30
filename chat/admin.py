from django.contrib import admin

# Register your models here.
from .models import Message

# Register your models here.


class MessageAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"

    # to filter the resultes by users, content types and action flags
    list_filter = [
        "sent_by",
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        "sent_by",
        "created_by",
    ]

    list_display = [
        "id",
        "body",
        "sent_by",
        "created_at",
        "created_by",
    ]


admin.site.register(Message, MessageAdmin)
