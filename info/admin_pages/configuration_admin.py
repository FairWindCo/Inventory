from django.contrib import admin
from django.contrib.admin import display


class ConfigurationServerAdmin(admin.ModelAdmin):
    list_display = ('display_server', 'platform_name', 'num_cpu', 'num_cores', 'num_virtual', 'ram')
    search_fields = ('server__name', 'platform_name')
    list_filter = ('server__name',)
    ordering = ('server__name',)
    save_as = True

    @display(description='Сервер')
    def display_server(self, obj):
        return obj.server.name


class DiskAdmin(admin.ModelAdmin):
    list_display = ('display_server', 'pool_name', 'hdd_size', 'hdd_type', 'raid_type')
    search_fields = ('configuration__server__name', 'pool_name')
    list_filter = ('configuration__server__name',)
    ordering = ('configuration__server__name',)
    save_as = True

    @display(description='Сервер')
    def display_server(self, obj):
        return obj.configuration.server.name
