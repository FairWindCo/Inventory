from django.contrib import admin
from django.contrib.admin import display


class HostInstalledSoftwareAdmin(admin.ModelAdmin):
    list_display = ('get_server_name', 'get_soft_name', 'version',
                    'installation_date', )
    search_fields = ('server__name', 'soft__name')
    sortable_by = ('get_server_name', 'get_soft_name')
    ordering = ('server__name', 'soft__name')
    autocomplete_fields = ('server', 'soft')
    list_filter = ('server__name', )
    save_as = True

    @display(ordering='name', description='Server')
    def get_server_name(self, obj):
        return obj.server.name

    @display(ordering='name', description='Soft')
    def get_soft_name(self, obj):
        return obj.soft.name


class HostScheduledTaskAdmin(admin.ModelAdmin):
    list_display = ('get_server_name', 'get_task_name',
                    # 'installation_date',
                    'last_run', 'next_run')
    search_fields = ('server__name', 'task__name')
    sortable_by = ('get_server_name', 'get_task_name')
    ordering = ('server__name', 'task__name')
    autocomplete_fields = ('server', 'task')
    list_filter = ('server__name', 'task__silent')
    save_as = True

    @display(ordering='name', description='Server')
    def get_server_name(self, obj):
        return obj.server.name

    @display(ordering='name', description='Soft')
    def get_task_name(self, obj):
        return obj.task.name


# class SoftAdminProxy(Server):
#     class Meta:
#         proxy = True
#         verbose_name = 'Состояние Серверов'
#         verbose_name_plural = 'Состояние Серверов'
