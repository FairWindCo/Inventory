from django.contrib.admin import display
from django.contrib.admin.utils import quote
from django.urls import reverse
from django.utils.safestring import mark_safe

from django_helpers.admin.change_title_admin import ChangeTitleAdminModel
from info.models import Server
from reports.admin_pages.multi_lookup import StatusListFilter


class ServerInfoAdminProxy(Server):
    help_text = 'Перелік інформації, про всі зареєстровані сервери ' \
                '(при виборі окремого стерверу відкривається додаткова інформація)'
    form_help_text = 'Інформація про один конкретний сервер'
    tooltip = 'Загальна інформація про сервер'

    class Meta:
        proxy = True
        verbose_name = '1. Сервери'
        verbose_name_plural = '1. Сервери'


class ServerInfoViewAdmin(ChangeTitleAdminModel):
    list_display_links = None
    list_display = ('room', 'domain', 'show_url_with_description', 'ip_address_set',
                    'virtual_server_name', 'os_name', 'os_version', 'status', 'os_last_update')
    readonly_fields = ('show_url_with_description',
        'show_configuration', 'show_application', 'show_soft', 'show_roles', 'show_tasks', 'show_daemons')
    exclude = ('futures', 'daemons')
    autocomplete_fields = ('os_name',)
    search_fields = ('name', 'ip_addresses__ip_address', 'virtual_server_name')
    list_filter = (StatusListFilter, 'external', 'room', 'domain', 'os_name__name', 'applications__name',)

    fieldsets = (
        ('Загальне', {
            'fields': ('room', 'domain', 'ip_address_set',
                       'name', 'virtual_server_name', 'os_name', 'os_version', 'status',),
            'classes': ('baton-tabs-init', 'baton-tab-fs-conf', 'baton-tab-fs-serv', 'baton-tab-fs-roles',
                        'baton-tab-fs-demons', 'baton-tab-fs-soft', 'baton-tab-fs-task', 'baton-tab-fs-other',
                        'baton-tab-fs-admin',
                        ),
        }
         ),
        ('Конфігурація', {
            'fields': ('show_configuration',),
            'classes': ('tab-fs-conf',),
            'description': 'Апаратна конфігурація сервера'
        }),
        ('Сервіси', {
            'fields': ('show_application',),
            'classes': ('tab-fs-serv',),
            'description': 'Сервіси в яких задіяни даний сервер'
        }),
        ('Ролі', {
            'fields': ('show_roles',),
            'classes': ('tab-fs-roles',),
            'description': 'Системні ролі, що втановлено на сервер'
        }),
        ('Служби', {
            'fields': ('show_daemons',),
            'classes': ('tab-fs-demons',),
            'description': 'Служби, що запущені на сервері'
        }),
        ('Софт', {
            'fields': ('show_soft',),
            'classes': ('tab-fs-soft',),
            'description': 'ПО встановлено на сервері'
        }),
        ('Таски', {
            'fields': ('show_tasks',),
            'classes': ('tab-fs-task',),
            'description': 'Автоматичні завдання, що виконується на сервері'
        }),
        ('Різне', {
            'fields': ('description', 'replaced_by', 'os_last_update', 'last_update_id', 'win_rm_access', 'external',
                       'has_internet_access', 'has_monitoring_agent', 'os_installed',),
            'classes': ('tab-fs-other',),
        }),
        ('Адміністративні', {
            'fields': ('created_at', 'updated_at', 'updated_by', 'version'),
            'classes': ('tab-fs-admin',),
        }),

    )
    @display(description='Ім\'я сервера')
    def show_url_with_description(self, obj):
        opts = obj._meta
        obj_url = reverse(
            "admin:%s_%s_change" % (opts.app_label, opts.model_name),
            args=(quote(obj.pk),),
            current_app=self.admin_site.name,
        )
        if obj.description:
            return mark_safe(f"<a href='{obj_url}' class='fw_tooltip'>{obj.name}"
                             f"<span class='tooltiptext tooltiplong'>{obj.description}</span></a>")
        else:
            return mark_safe(f"<a href='{obj_url}'>{obj.name}</a>")
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

    @display(description='Сервіс')
    def show_application(self, obj):
        infos = []
        for app in obj.app_info.all():
            for spec in app.specification.all():
                url = reverse('admin:{}_{}_change'.format('reports', 'appinfoaproxy'), args=(app.application.id,))
                infos.append(f'<a href={url}>{app.application.name if app.application else ""} - '
                             f'{spec.response.name if spec.response else ""}'
                             f' ({spec.role.name if spec.role else ""})</a>')
        return mark_safe('<BR>'.join(infos))

    @display(description='ПО')
    def show_soft(self, obj):
        infos = [f'<a href="{ServerInfoViewAdmin.get_change_url(app)}">{app.soft.name} - {app.version}</a>'
                 for app in obj.host_soft.
                 filter(soft__silent=False).
                 order_by('soft__name').
                 all()]
        return mark_safe('<BR>'.join(infos))

    @display(description='Системні ролі (Futures)')
    def show_roles(self, obj):
        infos = [
            f'<a href="{ServerInfoViewAdmin.get_change_url(app)}">{app.name} {"- " + app.display_name if app.display_name else ""}</a>'
            for app in obj.futures.
            filter(silent=False).order_by('name').all()]
        # print(infos)
        return mark_safe('<BR>'.join(infos))

    @display(description='Заплановані завдання')
    def show_tasks(self, obj):
        infos = [f'<a href="{ServerInfoViewAdmin.get_change_url(app)}">{app.name} [{app.execute_path}]</a>'
                 for app in obj.scheduled_tasks.
                 filter(silent=False).
                 order_by('name').
                 all()]
        # print(infos)
        return mark_safe('<BR>'.join(infos))

    @display(description='Служби (Services)')
    def show_daemons(self, obj):
        infos = [
            f'<a href="{ServerInfoViewAdmin.get_change_url(app)}">{app.name} {"- " + app.display_name if app.display_name else ""}</a>'
            for app in obj.daemons.filter(silent=False).all()]
        # print(infos)
        return mark_safe('<BR>'.join(infos))

    @staticmethod
    def get_change_url(obj):
        app_label = obj._meta.app_label
        model = obj._meta.model_name
        return reverse('admin:%s_%s_change' % (app_label, model), args=(obj.id,))

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
