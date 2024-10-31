""" Custom admin site for the Template model
"""
from django import forms
from django.contrib import admin

from core_main_app.components.template.models import Template


class TemplateAdminForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = "__all__"
        labels = {
            "is_current": "Current version",
            "is_disabled": "Version disabled",
        }
        help_texts = {
            "is_current": "About this version only, not the family's enabled/disabled status below.",
            "is_disabled": "About this version only, not the family's enabled/disabled status below.",
        }


class CustomTemplateAdmin(admin.ModelAdmin):
    """CustomTemplateAdmin"""

    form = TemplateAdminForm
    readonly_fields = ["checksum", "hash", "file", "version_manager_status"]
    exclude = ["_cls"]
    list_display = [
        "filename",
        "format",
        "version_manager",
        "is_version_manager_active",
    ]
    list_filter = ["format", "version_manager__is_disabled"]
    search_fields = ["filename"]

    @admin.display(
        description="Active", boolean=True, ordering="version_manager__is_disabled"
    )
    def is_version_manager_active(self, obj):
        """Active/disabled status lives on the version manager (the template
        family), not on this individual version -- Template's own
        is_current/is_disabled fields are unused in this deployment (every
        version manager here has exactly one version)."""
        return bool(obj.version_manager and not obj.version_manager.is_disabled)

    @admin.display(description="Template family status")
    def version_manager_status(self, obj):
        """Is_current/is_disabled below are about THIS version only. This
        shows the family-level status separately, since the two can
        legitimately disagree (e.g. a disabled family's only version still
        correctly reads as "current")."""
        if not obj.version_manager:
            return "No version manager"
        return (
            "Family is DISABLED"
            if obj.version_manager.is_disabled
            else "Family is active"
        )

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding Templates"""
        return False
