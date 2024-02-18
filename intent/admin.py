from django.contrib import admin
# from import_export.admin import ImportExportMixin
from intent.models import Event, ResponseText, IntentEventAction, Intent, IntentExample, IntentResponseEvent
# Register your models here.


class EventAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    list_display = [
        "name",
        "description",
        "trigger_condition",
        "agent",
    ]


admin.site.register(Event, EventAdmin)


class InlineResponseText(admin.TabularInline):
    model = ResponseText
    extra = 1


class IntentEventActionAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    inlines = [InlineResponseText]
    save_as = True
    list_display = [
        "name",
        "description",
        "response_type",
        "agent",
    ]


admin.site.register(IntentEventAction, IntentEventActionAdmin)


class InlineIntentExample(admin.TabularInline):
    model = IntentExample
    extra = 1


class InlineIntentResponseEvent(admin.TabularInline):
    model = IntentResponseEvent
    extra = 1


class IntentAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    inlines = [InlineIntentExample, InlineIntentResponseEvent]
    list_display = [
        "name",
        "description",
        "agent",
    ]


admin.site.register(Intent, IntentAdmin)
