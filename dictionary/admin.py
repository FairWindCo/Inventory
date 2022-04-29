from django.contrib import admin

from .models import *


# Register your models here.
class SimpleNameAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    sortable_by = ('name',)


class IPAdmin(admin.ModelAdmin):
    search_fields = ('ip_address',)
    sortable_by = ('ip_address',)


class SoftwareCatalogAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    sortable_by = ('name',)


class RoomAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    sortable_by = ('name',)
    autocomplete_fields = ('net_masks',)


admin.site.register(SoftwareCatalog, SoftwareCatalogAdmin)
admin.site.register(IP, IPAdmin)
admin.site.register(OS, SimpleNameAdmin)
admin.site.register(Domain, SimpleNameAdmin)
admin.site.register(ServerRoom, RoomAdmin)
admin.site.register(ServerRole, SimpleNameAdmin)
admin.site.register(ServerFuture, SimpleNameAdmin)
admin.site.register(ServerResponse, SimpleNameAdmin)
admin.site.register(ServerService, SimpleNameAdmin)
