from nested_admin.nested import NestedModelAdmin

from info.admin_pages.inline_admins import ServerSpecificationInlineAdmin


class ServerAdmin(NestedModelAdmin):
    list_display_links = ('name',)
    list_display = ('room', 'domain', 'ip_address_set',
                    'name', 'virtual_server_name', 'os_name', 'os_version', 'status')
    autocomplete_fields = ('domain', 'room', 'os_name', 'ip_addresses', 'futures', 'daemons', 'replaced_by')
    filter_horizontal = ('ip_addresses', 'futures')
    search_fields = ('name', 'ip_addresses__ip_address', 'virtual_server_name')
    list_filter = ('room', 'domain', 'os_name__name', 'status', 'replaced_by__name')
    save_as = True
    actions_on_top = True
    inlines = [ServerSpecificationInlineAdmin,
               ]

    fieldsets = (
        ('Загальне', {
            'fields': ('room', 'domain', 'ip_addresses',
                       'name', 'virtual_server_name', 'os_name', 'os_version', 'status',),
            'classes': ('baton-tabs-init', 'baton-tab-fs-upd', 'baton-tab-fs-roles',
                        'baton-tab-fs-demons', 'baton-tab-fs-other',
                        'baton-tab-inline-app_info', 'baton-tab-fs-desc',
                        ),
        }
         ),
        ('Апдейти', {
            'fields': ('os_installed', 'os_last_update', 'os_update_search', 'last_update_id',),
            'classes': ('tab-fs-upd',),
            'description': 'Сервіси в яких задіяни даний сервер'
        }),
        ('Ролі', {
            'fields': ('futures',),
            'classes': ('tab-fs-roles',),
            'description': 'Системні ролі, що втановлено на сервер'
        }),
        ('Служби', {
            'fields': ('daemons',),
            'classes': ('tab-fs-demons',),
            'description': 'Служби, що запущені на сервері'
        }),
        ('Різне', {
            'fields': ('replaced_by',
                       'win_rm_access', 'has_internet_access', 'has_monitoring_agent',),
            'classes': ('tab-fs-other',),
        }),
        ('Опис', {
            'fields': ('description',),
            'classes': ('tab-fs-desc',),
        }),

    )

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
