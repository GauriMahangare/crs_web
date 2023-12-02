from django.contrib import admin


# Register your models here.

from .models import Agent


class AgentAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    # to filter the resultes by users, content types and action flags
    list_filter = [
        "name",
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        "name",
    ]

    list_display = [
        "name",
        "description"
    ]


admin.site.register(Agent, AgentAdmin)
