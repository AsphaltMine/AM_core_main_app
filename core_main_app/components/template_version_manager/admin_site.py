""" Custom admin site for the Template Version Manager model
"""
from django.contrib import admin


class CustomTemplateVersionManagerAdmin(admin.ModelAdmin):
    """CustomTemplateVersionManagerAdmin"""

    exclude = ["_cls"]
    search_fields = ["title"]
    list_filter = ["is_disabled", "user"]
    list_display = [
        "title",
        "is_active",
        "user",
        "display_rank",
        "creation_date",
    ]
    list_editable = ["display_rank"]

    @admin.display(description="Active", boolean=True, ordering="is_disabled")
    def is_active(self, obj):
        return not obj.is_disabled

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding Template version managers"""
        return False
