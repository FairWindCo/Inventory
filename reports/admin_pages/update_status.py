from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.timezone import now

from django_helpers.admin.change_title_admin import ChangeTitleAdminModel
from info.models import Server
from remoting import run, update_update_date


class ServerAdminProxy(Server):
    help_text = 'Звіт про оновлення серверів'
    form_help_text = 'Інформація про оновлення конкретного серверу'
    tooltip = 'Звіт про оновлення серверів'

    class Meta:
        proxy = True
        verbose_name = 'Оновлення Серверів'
        verbose_name_plural = 'Оновлення Серверів'

    def days_from_update(self):
        if self.os_last_update:
            td = (now() - self.os_last_update).days
            if td < 0:
                color = 'red'
                td = 'ERROR'
            elif td < 7:
                color = 'green'
            elif td < 14:
                color = 'black'
            elif td < 30:
                color = 'orange'
            else:
                color = 'red'
            return mark_safe(f'<B style="color: {color}">{td}</B>')
        else:
            return 'немає даних'


@admin.action(description='Update Status refresh')
def make_refresh(modeladmin, request, queryset):
    run(update_update_date, server_list=queryset.all())


class ServerViewAdmin(ChangeTitleAdminModel):
    list_display_links = ('name',)
    list_display = ('name', 'domain', 'os_installed',
                    'os_name', 'os_version', 'os_last_update', 'days_from_update',
                    'os_update_search', 'last_update_id')
    autocomplete_fields = ('os_name',)
    search_fields = ('name', 'ip_addresses__ip_address', 'virtual_server_name')
    list_filter = ('room', 'domain', 'os_name__name')
    actions = [make_refresh]

    def get_search_results(self, request, queryset, search_term):
        return super().get_search_results(request, queryset, search_term)

    def get_queryset(self, request):
        return super().get_queryset(request)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
