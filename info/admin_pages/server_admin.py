from django.contrib import admin


class ServerAdmin(admin.ModelAdmin):
    list_display_links = ('name',)
    list_display = ('room', 'domain', 'ip_address_set',
                    'name', 'virtual_server_name', 'os_name', 'os_version', 'is_online')
    autocomplete_fields = ('domain', 'room', 'os_name', 'ip_addresses', 'futures', 'daemons')
    filter_horizontal = ('ip_addresses', 'futures')
    search_fields = ('name', 'ip_addresses__ip_address', 'virtual_server_name')
    list_filter = ('room', 'domain', 'os_name__name', 'is_online')
    save_as = True

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


