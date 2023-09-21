from django.contrib import admin

from .models import *


# Register your models here.
class SimpleNameAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    sortable_by = ('name',)


class OSNameAdmin(admin.ModelAdmin):
    search_fields = ('name', 'family')
    sortable_by = ('name', 'family', 'old')
    list_display = ('name', 'family', 'old')


class IPAdmin(admin.ModelAdmin):
    search_fields = ('ip_address',)
    sortable_by = ('ip_address',)


class SoftwareCatalogAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    sortable_by = ('name',)


class TaskCatalogAdmin(admin.ModelAdmin):
    list_display = ('name', 'execute_path')
    search_fields = ('name',)
    sortable_by = ('name',)


class RoomAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    sortable_by = ('name',)
    autocomplete_fields = ('net_masks',)


admin.site.register(SoftwareCatalog, SoftwareCatalogAdmin)
admin.site.register(IP, IPAdmin)
admin.site.register(OS, OSNameAdmin)
admin.site.register(Domain, SimpleNameAdmin)
admin.site.register(ServerRoom, RoomAdmin)
admin.site.register(ServerRole, SimpleNameAdmin)
admin.site.register(ServerFuture, SimpleNameAdmin)
admin.site.register(ServerResponse, SimpleNameAdmin)
admin.site.register(ServerService, SimpleNameAdmin)
admin.site.register(ServerScheduledTask, TaskCatalogAdmin)
