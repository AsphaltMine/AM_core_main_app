""" Custom admin site for the Workspace model
"""
from django import forms
from django.contrib import admin
from django.contrib.admin.helpers import ActionForm
from django.contrib.auth.models import User
from django.forms import ChoiceField
from django.utils.html import format_html

from core_main_app.components.user import api as user_api
from core_main_app.components.workspace.models import Workspace


class WorkspaceAdminForm(forms.ModelForm):
    """Shows/edits the owner as a username dropdown instead of a raw user id,
    since Workspace.owner is a plain CharField (not a real ForeignKey)."""

    owner = forms.ModelChoiceField(
        queryset=User.objects.order_by("username"),
        required=False,
        help_text="Leave empty for no owner (e.g. the global public workspace).",
    )

    class Meta:
        model = Workspace
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.owner:
            try:
                self.initial["owner"] = User.objects.get(pk=self.instance.owner)
            except User.DoesNotExist:
                pass
            self.fields["owner"].help_text = format_html(
                "Stored user ID: {}.<br>{}",
                self.instance.owner,
                self.fields["owner"].help_text,
            )

    def clean_owner(self):
        owner = self.cleaned_data.get("owner")
        return str(owner.pk) if owner else None


class UpdateWorkspaceActionForm(ActionForm):
    """Action form for workspace owner reassignment"""

    owner = ChoiceField(label="New owner:", required=False)

    def __init__(self, *args, **kwargs):
        owner_options = [("", "")]
        all_users = sorted(
            user_api.get_active_users(), key=lambda s: s.username.lower()
        )
        for user in all_users:
            owner_options.append((user.id, user.username))

        super().__init__(*args, **kwargs)
        self.fields["owner"].choices = owner_options


def update_workspace_owner(model_admin, request, queryset):
    """Reassign the owner of the selected workspaces

    Args:
        model_admin:
        request:
        queryset:

    Returns:

    """
    owner_id = request.POST.get("owner", "")
    if owner_id == "":
        return
    queryset.update(owner=str(owner_id))
    model_admin.message_user(request, f"Owner updated for {queryset.count()} workspace(s).")


class CustomWorkspaceAdmin(admin.ModelAdmin):
    """CustomWorkspaceAdmin"""

    form = WorkspaceAdminForm
    exclude = ["read_perm_id", "write_perm_id"]
    list_display = ["title", "owner_name", "is_public"]
    list_filter = ["is_public"]
    search_fields = ["title"]
    action_form = UpdateWorkspaceActionForm
    actions = [update_workspace_owner]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding Workspaces"""
        return False
