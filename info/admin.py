from django.contrib import admin
from django.contrib.admin.widgets import AdminTextInputWidget
from django.utils.safestring import mark_safe
from django.utils.timezone import now

from .models import *


# Register your models here.

class ServerAdmin(admin.ModelAdmin):
    list_display_links = ('name',)
    list_display = ('room', 'domain', 'ip_address_set',
                    'name', 'virtual_server_name', 'os_name', 'os_version', 'is_online')
    autocomplete_fields = ('domain', 'room', 'os_name', 'ip_addresses', 'roles', 'applications')
    filter_horizontal = ('ip_addresses', 'roles', 'applications')
    search_fields = ('name', 'ip_addresses__ip_address', 'virtual_server_name')
    list_filter = ('room', 'domain', 'os_name__name', 'applications__name')

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


# In models.py
class ServerAdminProxy(Server):
    class Meta:
        proxy = True
        verbose_name = 'Состояние Серверов'
        verbose_name_plural = 'Состояние Серверов'

    def days_from_update(self):
        if self.os_last_update:
            td = (now() - self.os_last_update).days
            if td < 0:
                color = 'red'
                td = 'ERROR'
            elif td < 7:
                color = 'green'
            elif td < 14:
                color = 'black'
            elif td < 30:
                color = 'orange'
            else:
                color = 'red'
            return mark_safe(f'<B style="color: {color}">{td}</B>')
        else:
            return 'нет данных'


class ServerViewAdmin(admin.ModelAdmin):
    list_display_links = ('name',)
    list_display = ('name', 'domain', 'os_installed',
                    'os_name', 'os_version', 'os_last_update', 'days_from_update',
                    'os_update_search', 'last_update_id')
    autocomplete_fields = ('os_name',)
    search_fields = ('name', 'ip_addresses__ip_address', 'virtual_server_name')
    list_filter = ('room', 'domain', 'os_name__name')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class SimpleNameAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    sortable_by = ('name',)


class IPAdmin(admin.ModelAdmin):
    search_fields = ('ip_address',)
    sortable_by = ('ip_address',)


class ApplicationAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('name',)
    fields = ['name', 'description', 'url', 'responsible']
    autocomplete_fields = ('responsible', )
    filter_horizontal = ('responsible', )


admin.site.register(Application, ApplicationAdmin)
admin.site.register(SoftwareCatalog, SimpleNameAdmin)
admin.site.register(IP, IPAdmin)
admin.site.register(OS, SimpleNameAdmin)
admin.site.register(Domain, SimpleNameAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(ServerAdminProxy, ServerViewAdmin)
admin.site.register(ServerRoom, SimpleNameAdmin)
admin.site.register(ServerRole, SimpleNameAdmin)
admin.site.register(ResponsiblePerson, SimpleNameAdmin)
