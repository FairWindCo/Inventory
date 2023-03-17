from django.contrib import admin
# Register your models here.
from django.contrib.admin import register, display

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
    search_fields = ('name', )


@register(TaskControl)
class ControlTaskReportAdmin(admin.ModelAdmin):
    list_display = ('show_name', 'code', 'last_execute')
    search_fields = ('host__name', 'code', 'message')
    autocomplete_fields = ('host', 'control_group')
    list_filter = ('host__name', 'code')
    readonly_fields = ('last_execute', 'last_control', 'last_message', 'message', 'status')

    @display(description='Сервер')
    def show_name(self, obj):
        return obj.host.name
