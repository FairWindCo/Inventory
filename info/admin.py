from django.contrib import admin
from .models import *


# Register your models here.

class ServerAdmin(admin.ModelAdmin):
    list_display_links = ('name',)
    list_display = ('room', 'domain', 'ip_address_set', 'name', 'virtual_server_name', 'os_name', 'is_online')
    autocomplete_fields = ('domain', 'room', 'os_name', 'ip_addresses', 'installed_soft', 'roles', 'applications')
    filter_horizontal = ('ip_addresses', 'installed_soft', 'roles', 'applications')
    search_fields = ('name', 'ip_addresses__ip_address', 'virtual_server_name')
    list_filter = ('room', 'domain', 'os_name__name')

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class SimpleNameAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    sortable_by = ('name',)


class IPAdmin(admin.ModelAdmin):
    search_fields = ('ip_address',)
    sortable_by = ('ip_address',)


admin.site.register(Application, SimpleNameAdmin)
admin.site.register(InstalledSoftware, SimpleNameAdmin)
admin.site.register(IP, IPAdmin)
admin.site.register(OS, SimpleNameAdmin)
admin.site.register(Domain, SimpleNameAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(ServerRoom, SimpleNameAdmin)
admin.site.register(ServerRole, SimpleNameAdmin)
