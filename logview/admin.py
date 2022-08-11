from django.contrib import admin
from django.contrib.admin import display

from .models import ServerModificationLog


# Register your models here.
class ServerLogViewAdmin(admin.ModelAdmin):
    list_display = ('seen', 'display_server', 'log_type', 'topic', 'description',)
    list_filter = ('log_type', 'topic', 'server__name',)
    ordering = ('-seen', 'server__name')

    @display(description='Сервер')
    def display_server(self, obj):
        return obj.server.name

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(ServerModificationLog, ServerLogViewAdmin)
