from django.contrib import admin
from django.contrib.admin import display
from django.utils.safestring import mark_safe

from info.models.applications import ApplicationServers, Application
from reports.admin_pages.servers_infos import ServerResponseInfoAdmin, ServersInApplicationInfoAdmin


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
        verbose_name = 'СЕРВІС'
        verbose_name_plural = '!СЕРВІСИ'


class ApplicationInfoAdmin(admin.ModelAdmin):
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


class ApplicationServerInfoAdmin(admin.ModelAdmin):
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
