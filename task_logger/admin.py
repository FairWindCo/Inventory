from django.contrib import admin
# Register your models here.
from django.contrib.admin import register, display

from dictionary.models import ServerScheduledTask
from task_logger.models import ServerTaskReport, TaskControl, TaskControlGroup


@register(ServerTaskReport)
class TastReportAdmin(admin.ModelAdmin):
    # list_display_links = ('show_name',)
    list_display = ('show_name', 'is_error', 'report_date', 'info',)
    search_fields = ('server__name', 'info')
    list_filter = ('server__name', 'is_error')

    @display(description='Конфигурация')
    def show_name(self, obj):
        return obj.server.name

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@register(TaskControlGroup)
class ControlGroupAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@register(TaskControl)
class ControlTaskReportAdmin(admin.ModelAdmin):
    list_display = ('show_name', 'show_code', 'last_execute', 'show_group', 'last_message')
    search_fields = ('host__name', 'code', 'message')
    autocomplete_fields = ('host', 'control_group')
    list_filter = ('host__name', 'code')
    readonly_fields = ('last_execute', 'last_control', 'last_message', 'message', 'status')

    @display(description='Сервер', ordering='host__name')
    def show_name(self, obj):
        return obj.host.name

    @display(description='Код задачі', ordering="code")
    def show_code(self, obj):
        try:
            task_info = ServerScheduledTask.objects.get(code=obj.code)
            return f'{obj.code} - {task_info.name}'
        except ServerScheduledTask.DoesNotExist:
            return obj.code

    @display(description='Група завдань', ordering='control_group__name')
    def show_group(self, obj):
        return obj.control_group.name if obj.control_group else '-'
