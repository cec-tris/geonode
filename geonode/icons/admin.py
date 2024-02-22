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
    

# [chumano] custom actstream
from actstream import models as amodels, admin as aadmin
try:
    from genericadmin.admin import GenericAdminModelAdmin as ModelAdmin
except ImportError:
    ModelAdmin = admin.ModelAdmin

class CustomActionAdmin(ModelAdmin):
    view_on_site = False
    date_hierarchy = 'timestamp'
    list_display = ('__str__', 'actor', 'verb', 'target', 'public')
    list_editable = ('verb',)
    list_filter = ('timestamp',)
    raw_id_fields = ('actor_content_type', 'target_content_type',
                     'action_object_content_type')
    def has_change_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False

#print(aadmin.ActionAdmin)   
admin.site.unregister(amodels.Action)
admin.site.register(amodels.Action, CustomActionAdmin)