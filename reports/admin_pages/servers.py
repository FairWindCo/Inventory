from django.contrib import admin
from django.contrib.admin import display
from django.utils.safestring import mark_safe

from info.models import Server


class ServerInfoAdminProxy(Server):
    class Meta:
        proxy = True
        verbose_name = 'СЕРВЕР'
        verbose_name_plural = '!СЕРВЕРИ'


class ServerInfoViewAdmin(admin.ModelAdmin):
    list_display_links = ('name',)
    list_display = ('room', 'domain', 'ip_address_set',
                    'name', 'virtual_server_name', 'os_name', 'os_version', 'is_online', 'os_last_update')
    readonly_fields = ('show_configuration', 'show_application', 'show_soft', 'show_roles', 'show_daemons')
    exclude = ('futures', 'daemons')
    autocomplete_fields = ('os_name',)
    search_fields = ('name', 'ip_addresses__ip_address', 'virtual_server_name')
    list_filter = ('external', 'room', 'domain', 'os_name__name', 'applications__name', )

    @display(description='Конфігурація')
    def show_configuration(self, obj):
        infos = []
        for hardware in obj.hardware.all():
            infos.append(f'{hardware.platform_name}<BR> {hardware.cpu_type} <B>CPU:</B>{hardware.num_cpu} '
                         f'<B>CORE:</B>{hardware.num_cores} <B>HT:</B>{hardware.num_virtual} <B>RAM:</B> '
                         f'{hardware.ram}GB'
                         )
            for disk in hardware.disks.all():
                hdd_type = disk.get_hdd_type_display()
                if hdd_type is None:
                    hdd_type = ''
                else:
                    hdd_type = f'{hdd_type}'
                infos.append(f'{disk.pool_name if disk.pool_name else ""} {hdd_type} - {disk.hdd_size}Gb')
        return mark_safe('<BR>'.join(infos))

    @display(description='Додаток')
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

    @display(description='ПО')
    def show_soft(self, obj):
        infos = [f'{app.soft.name} - {app.version}'
                 for app in obj.host_soft.all()]
        return mark_safe('<BR>'.join(infos))

    @display(description='Ролі')
    def show_roles(self, obj):
        infos = [f'{app.name} {"- " + app.display_name if app.display_name else ""}'
                 for app in obj.futures.all()]
        # print(infos)
        return mark_safe('<BR>'.join(infos))

    @display(description='Служби')
    def show_daemons(self, obj):
        infos = [f'{app.name} {"- " + app.display_name if app.display_name else ""}'
                 for app in obj.daemons.all()]
        # print(infos)
        return mark_safe('<BR>'.join(infos))

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
