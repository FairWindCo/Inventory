from django.contrib import admin
# Register your models here.
from django.contrib.admin import register, display

from task_logger.models import ServerTaskReport


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

