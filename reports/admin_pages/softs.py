from django.contrib import admin
from django.contrib.admin import display
from django.utils.safestring import mark_safe

from dictionary.models import SoftwareCatalog
from info.models import HostInstalledSoftware


class SoftInfoAdminProxy(SoftwareCatalog):
    class Meta:
        proxy = True
        verbose_name = 'Программы'
        verbose_name_plural = 'Программы'


class SoftInfoAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = (
        'name',)
    readonly_fields = ('display_servers',)
    list_filter = ('installs__server__name',)

    @display(description='URL')
    def display_servers(self, obj):
        infos = [f'<B>{insttals.server.name}:</b> {insttals.soft.name} - {insttals.version}'
                 for insttals in obj.installs.all()]
        return mark_safe('<BR>'.join(infos))

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class InstalledSoftInfoAdminProxy(HostInstalledSoftware):
    class Meta:
        proxy = True
        verbose_name = 'Установленные программы'
        verbose_name_plural = 'Установленные программы'


class InstalledSoftInfoAdmin(admin.ModelAdmin):
    search_fields = ('soft__name', 'server__name', 'version')
    list_display = ('display_application', 'display_server', 'version', 'installation_date', 'is_removed')
    list_filter = ('server__name', 'is_removed')

    @display(description='Сервер')
    def display_server(self, obj):
        return obj.server.name

    @display(description='Приложение')
    def display_application(self, obj):
        return obj.soft.name


    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
