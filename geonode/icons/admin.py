from django.contrib import admin
from django.utils.html import format_html
from .models import Icon

@admin.register(Icon)
class IconAdmin(admin.ModelAdmin):
    list_display = ("name", "image_icon", "path", "uploaded_at")
    fields = ["name", "path",'image_tag']
    readonly_fields = ['image_tag']

    def image_icon(self, obj):
        return format_html('<img width="32" src="{}" />'.format(obj.path.url))