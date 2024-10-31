""" Custom admin site for the Template Xsl Rendering model
"""
from django.contrib import admin


class CustomTemplateXslRenderingAdmin(admin.ModelAdmin):
    """CustomTemplateXslRenderingAdmin"""

    list_display = ["template", "list_xslt", "default_detail_xslt"]
    search_fields = ["template__filename"]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding Template Xsl rendering"""
        return False
