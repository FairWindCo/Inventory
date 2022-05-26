from django.contrib import admin
from django.contrib.admin import display
from django.utils.safestring import mark_safe

from dictionary.models import ServerFuture, ServerService


class FutureAdminProxy(ServerFuture):
    class Meta:
        proxy = True
        verbose_name = 'Роль'
        verbose_name_plural = 'Ролі'


class SoftFutureAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = (
        'name',)
    readonly_fields = ('display_servers',)
    list_filter = ('servers__name',)

    @display(description='Сервери')
    def display_servers(self, obj):
        infos = [f'{server.name}'
                 for server in obj.servers.all()]
        return mark_safe('<BR>'.join(infos))

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class DaemonsAdminProxy(ServerService):
    class Meta:
        proxy = True
        verbose_name = 'Служба'
        verbose_name_plural = 'Служби'


class DaemonsAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = (
        'name',)
    readonly_fields = ('display_servers',)
    list_filter = ('servers__name',)

    @display(description='Сервери')
    def display_servers(self, obj):
        infos = [f'{server.name}'
                 for server in obj.servers.all()]
        return mark_safe('<BR>'.join(infos))

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
