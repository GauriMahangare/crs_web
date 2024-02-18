from django.contrib import admin
# from import_export.admin import ImportExportMixin

from entity.models import Entity, EntityTypes

# Register your models here.


class EntityTypesAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    # to filter the resultes by users, content types and action flags
    list_filter = [
        "type",
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        "name",
        "agent",
        "type",
    ]

    list_display = [
        "name",
        "description",
        "type",
        "agent",
    ]


admin.site.register(EntityTypes, EntityTypesAdmin)


class EntityAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    list_display = [
        "name",
        "description",
        "synonyms",
        "exclude",
        "agent",
    ]


admin.site.register(Entity, EntityAdmin)
