from django.contrib import admin
from django.contrib.admin import display
from django.utils.safestring import mark_safe

from info.models import Server


class ServerInfoAdminProxy(Server):
    class Meta:
        proxy = True
        verbose_name = '!СЕРВЕР'
        verbose_name_plural = '!СЕРВЕРА'


class ServerInfoViewAdmin(admin.ModelAdmin):
    list_display_links = ('name',)
    list_display = ('room', 'domain', 'ip_address_set',
                    'name', 'virtual_server_name', 'os_name', 'os_version', 'is_online', 'os_last_update')
    readonly_fields = ('show_configuration', 'show_application', 'show_soft', 'show_roles')
    exclude = ('futures',)
    autocomplete_fields = ('os_name',)
    search_fields = ('name', 'ip_addresses__ip_address', 'virtual_server_name')
    list_filter = ('room', 'domain', 'os_name__name', 'applications__name')

    @display(description='Конфигурация')
    def show_configuration(self, obj):
        infos = []
        for hardware in obj.hardware.all():
            infos.append(f'{hardware.platform_name} <B>CPU:</B>{hardware.num_cpu} '
                         f'<B>CORE:</B>{hardware.num_cores} <B>HT:</B>{hardware.num_virtual} <B>RAM:</B> '
                         f'{hardware.ram}GB'
                         )
            for disk in hardware.disks.all():
                hdd_type = disk.get_hdd_type_display()
                if hdd_type is None:
                    hdd_type = ''
                else:
                    hdd_type = f'{hdd_type}'
                infos.append(f'{disk.pool_name} {hdd_type} - {disk.hdd_size}Gb')
        return mark_safe('<BR>'.join(infos))

    @display(description='Приложения')
    def show_application(self, obj):
        infos = []
        for app in obj.app_info.all():
            for spec in app.specification.all():
                print(app.application.name)
                print(spec.response.name)
                print(spec.role.name)
                infos.append(f'{app.application.name} - '
                             f'{spec.response.name}'
                             f' ({spec.role.name})')
        return mark_safe('<BR>'.join(infos))

    @display(description='Программы')
    def show_soft(self, obj):
        infos = [f'{app.soft.name} - {app.version}'
                 for app in obj.host_soft.all()]
        return mark_safe('<BR>'.join(infos))

    @display(description='Роли')
    def show_roles(self, obj):
        infos = [f'{app.name} - {app.display_name}'
                 for app in obj.futures.all()]
        # print(infos)
        return mark_safe('<BR>'.join(infos))

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
