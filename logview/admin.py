from django.contrib import admin

from .models import ServerModificationLog


# Register your models here.
class ServerLogViewAdmin(admin.ModelAdmin):
    # list_display_links = ('name',)
    # list_display = ('name', 'domain', 'os_installed',
    #                 'os_name', 'os_version', 'os_last_update', 'days_from_update',
    #                 'os_update_search', 'last_update_id')
    # autocomplete_fields = ('os_name',)
    # search_fields = ('name', 'ip_addresses__ip_address', 'virtual_server_name')
    # list_filter = ('room', 'domain', 'os_name__name')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.register(ServerModificationLog, ServerLogViewAdmin)
