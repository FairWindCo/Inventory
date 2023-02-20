from django.contrib import admin
from django.contrib.admin import display
from django.utils.safestring import mark_safe

from dictionary.models import SoftwareCatalog
from django_helpers.admin.change_title_admin import ChangeTitleAdminModel
from info.models import HostInstalledSoftware


class SoftInfoAdminProxy(SoftwareCatalog):
    help_text = 'Перелік встановлених на серверах програмах' \
                '(при виборі окремої програми відриється інформація на яких серверах вона встановлена)'
    form_help_text = 'Конкретна программа, та перелік серверів де вона встановлена'
    tooltip = 'Інформація про софт, що встановлено на серверах'

    class Meta:
        proxy = True
        verbose_name = 'Програми'
        verbose_name_plural = 'Програми'


class SoftInfoAdmin(ChangeTitleAdminModel):
    search_fields = ('name',)
    list_display = (
        'name',)
    readonly_fields = ('display_servers',)
    list_filter = ('installs__server__name',)

    @display(description='Сервери')
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
        verbose_name = 'Встановленне ПЗ'
        verbose_name_plural = 'Встановлення ПЗ'


class InstalledSoftInfoAdmin(ChangeTitleAdminModel):
    search_fields = ('soft__name', 'server__name', 'version')
    list_display = ('display_application', 'display_server', 'version', 'installation_date', 'is_removed')
    list_filter = ('server__name', 'is_removed')

    @display(description='Сервер')
    def display_server(self, obj):
        return obj.server.name

    @display(description='Додаток')
    def display_application(self, obj):
        return obj.soft.name


    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
