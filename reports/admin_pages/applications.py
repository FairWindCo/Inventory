from django.contrib import admin
from django.contrib.admin import display
from django.urls import reverse
from django.utils.safestring import mark_safe

from django_helpers.admin.change_title_admin import ChangeTitleAdminModel
from info.models.applications import ApplicationServers, Application
from reports.admin_pages.servers_infos import ServerResponseInfoAdmin


class AppInfoAdminProxy(ApplicationServers):
    help_text = 'Звіт описує які портали\додатки з якими серверами пов\'язіні'
    form_help_text = 'Цей портал або дадаток залежить від роботи наступних серверів'

    class Meta:
        proxy = True
        verbose_name = '3. Зв\'язок порталів та серверів'
        verbose_name_plural = '3. Зв\'язок порталів та серверів'


class AppInfoAProxy(Application):
    class Meta:
        proxy = True
        verbose_name = '2. Сервіси'
        verbose_name_plural = '2. Сервіси'


class ApplicationServerInfoAdmin(ChangeTitleAdminModel):
    search_fields = ('application__name', 'server__name')
    list_display = (
        'display_application', 'display_server', 'display_url', 'display_note')
    list_filter = ('application__name', 'server__name',)

    inlines = [ServerResponseInfoAdmin]

    @display(description='Сервер')
    def display_server(self, obj):
        return obj.server.name

    @display(description='Додаток')
    def display_application(self, obj):
        return obj.application.name

    @display(description='URL')
    def display_url(self, obj):
        return mark_safe(f'<a href="{obj.application.url}">{obj.application.url}</a>') if obj.application.url else '-'

    @display(description='Роль')
    def display_role(self, obj):
        return obj.role.name if obj.role else '-'

    @display(description='Відповідальність')
    def display_response(self, obj):
        return obj.response.name if obj.response else '-'

    @display(description='Примітка')
    def display_note(self, obj):
        if len(obj.description) > 40:
            return f'{obj.description[:40]}...'
        else:
            return obj.description

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class InlineModelApplicationServersProxy(AppInfoAdminProxy):
    class Meta:
        proxy = True
        verbose_name = 'Задіяний сервер'
        verbose_name_plural = 'Задіяні сервери'


class ServersInApplicationInfoAdmin(admin.TabularInline):
    template = 'admin/edit_inline/tabular_spec.html'
    fields = ("display_special_name", 'description', 'server_specifications')
    readonly_fields = ("display_special_name", 'server_specifications',)
    show_change_link = False
    model = InlineModelApplicationServersProxy
    extra = 0

    @display(description='Сервер')
    def display_special_name(self, obj):
        url = reverse('admin:{}_{}_change'.format('reports', 'serverinfoadminproxy'), args=(obj.server.id,))
        return mark_safe(
            f'<a href="{url}">{obj.server.canonical_name if obj.server.canonical_name else obj.server.name}</a>')


    @staticmethod
    def form_server_specification(spec_info):
        server_role = f'Роль: {spec_info.role.name} ' if spec_info.role else ''
        server_resp = f'{spec_info.response.name} ' if spec_info.response else ''
        desc = [f'<b>{server_role} - {server_resp}</b>' if server_role else f'<b>{server_resp}</b>']
        if spec_info.response_person:
            desc.append(f'Відповідальний: {spec_info.response_person}')
        if spec_info.description:
            desc.append(f'Примітка:{spec_info.description}')
        return '<br>'.join(desc)
    @display(description='Зона відповідальності')
    def server_specifications(self, obj):
        return mark_safe('<BR>'.join([self.form_server_specification(spec_info)
                                      for spec_info in obj.specification.all()]))

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ApplicationInfoAdmin(ChangeTitleAdminModel):
    fields = (
        'name', 'display_url', 'display_monitor_url', 'description', 'external', 'depends', 'display_dependency')
    search_fields = ('name', 'app_server__server__name', 'url')
    list_display = (
        'name', 'display_url', 'display_monitor_url')
    list_filter = ('external', 'name', 'app_server__server__name',)

    @display(description='URL')
    def display_url(self, obj):
        return mark_safe(f'<a href="{obj.url}">{obj.url}</a>') if obj.url else '-'

    @display(description='Моніторінг URL')
    def display_monitor_url(self, obj):
        return mark_safe(f'<a href="{obj.monitoring_url}">{obj.monitoring_url}</a>') if obj.monitoring_url else '-'

    inlines = [ServersInApplicationInfoAdmin]

    @display(description='Необхідна для')
    def display_dependency(self, obj):
        infos = [f'{server.name}'
                 for server in obj.dependencies.all()]
        return mark_safe('<BR>'.join(infos))

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
