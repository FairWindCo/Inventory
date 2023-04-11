import datetime

from django.contrib import admin
from django.contrib.admin import display
from django.utils.safestring import mark_safe

from dictionary.models import ServerFuture, ServerService
from django_helpers.admin.defaut_filter_value_mixin import DefaultFilterMixin
from info.models.applications import HostScheduledTask


class FutureAdminProxy(ServerFuture):
    help_text = 'Перелік існуючих Future в системі ' \
                '(якщо вибрати конкретне значення, то буде виведено перелік серверів де вона встановлена)'
    form_help_text = 'Перелік серверів де встановлена відповідна Future'

    class Meta:
        proxy = True
        verbose_name = 'Роль'
        verbose_name_plural = 'Ролі'


class ServerTaskAdminProxy(HostScheduledTask):
    help_text = 'Перелік існуючих ScheduledTask про які є інформацыя в системы ' \
                '(якщо вибрати конкретне значення, то буде виведено перелік серверів де вони виконуються)'
    form_help_text = 'Перелік серверів де відповідний ScheduledTask встановлено'

    class Meta:
        proxy = True
        verbose_name = 'Заплановані Задачі'
        verbose_name_plural = 'Заплановані Задачі'


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


class ServerTaskAdmin(DefaultFilterMixin, admin.ModelAdmin):
    search_fields = ('task__name', 'server__name')
    list_display = ('display_server', 'display_task', 'display_scheduller',
                    'display_execution', 'exit_code', 'comments')
    readonly_fields = ('display_server', 'display_task', 'server', 'task',
                       'last_run', 'next_run', 'exit_code', 'is_removed',
                       'run_user', 'author', 'schedule_type', 'installation_date',
                       'last_check_date', 'status')
    list_filter = ('server__name', 'task__name', 'is_removed', 'task__silent')
    default_filters = (
        ('is_removed__exact', 0),
        ('task__silent__exact', 0),
    )

    def get_queryset(self, request):
        print("test")
        return super().get_queryset(request)

    @display(description='Планування')
    def display_scheduller(self, obj):
        if obj.schedule_type:
            return mark_safe(obj.form_html_schedule_type())
        return obj.schedule_type


    @display(description='Останній \ Наступний запуск ')
    def display_execution(self, obj):

        run =obj.last_run.strftime("%d-%m-%Y %H:%M:%S") if obj.last_run else '-'
        next = obj.next_run.strftime("%d-%m-%Y %H:%M:%S") if obj.next_run else '-'
        return mark_safe(f'{run}<BR>{next}')



    @display(description='Сервер', ordering='server__name')
    def display_server(self, obj):
        return obj.server.name

    @display(description='Назва задачі', ordering='task__name')
    def display_task(self, obj):
        return mark_safe(obj.form_task_name())

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False


class DaemonsAdminProxy(ServerService):
    help_text = 'Перелік існуючих Service про які є інформацыя в системы ' \
                '(якщо вибрати конкретне значення, то буде виведено перелік серверів де вони виконуються)'
    form_help_text = 'Перелік серверів де відповідний Service запущено'

    class Meta:
        proxy = True
        verbose_name = 'Служба (Service)'
        verbose_name_plural = 'Служби (Service)'


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
