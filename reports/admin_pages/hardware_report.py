from django.contrib.admin import display
from django.contrib.admin.utils import quote
from django.urls import reverse
from django.utils.safestring import mark_safe

from django_helpers.admin.change_title_admin import ChangeTitleAdminModel
from info.models import Configuration


class ServerHardwareInfoAdminProxy(Configuration):
    help_text = 'Перелік конфігурацій, про всі зареєстровані сервери '
    form_help_text = 'Інформація про один вибраний сервер'
    tooltip = 'Загальна інформація про сервер'

    class Meta:
        proxy = True
        verbose_name = '    Конфігурації серверів'
        verbose_name_plural = 'Конфігурація сервера'


class HardwareInfoViewAdmin(ChangeTitleAdminModel):
    list_display_links = None
    list_display = (
        'show_url_with_description', 'show_room', 'show_ips', 'show_config_desc', 'num_cpu', 'num_virtual', 'ram'
    )
    search_fields = (
    'server__name', 'server__ip_addresses__ip_address', 'server__virtual_server_name', 'platform_name', 'cpu_type')
    list_filter = ('server__room', 'server__domain', 'server__os_name__name',)

    #    list_display = ('server__room',
    # 'domain', 'show_url_with_description', 'show_ips',
    # 'virtual_server_name'
    #                   )
    @display(description='Ім\'я сервера')
    def show_url_with_description(self, obj):
        opts = obj.server._meta
        obj_url = reverse(
            "admin:%s_%s_change" % (opts.app_label, opts.model_name),
            args=(quote(obj.pk),),
            current_app=self.admin_site.name,
        )
        if obj.server.description:
            return mark_safe(f"<a href='{obj_url}' class='fw_tooltip'>{obj.server.name}"
                             f"<span class='tooltiptext tooltiplong'>{obj.server.description}</span></a>")
        else:
            return mark_safe(f"<a href='{obj_url}'>{obj.server.name}</a>")

    @display(description='Ім\'я сервера')
    def show_room(self, obj):
        return obj.server.room

    @display(description='Конфігурація')
    def show_config_desc(self, obj):
        describe = []
        if obj.platform_name:
            describe.append(obj.platform_name)
        if obj.description:
            describe.append(obj.description)
        if obj.cpu_type:
            describe.append(obj.cpu_type)
        disks = obj.disks.all()
        if disks:
            for disk in disks:
                describe.append(str(disk))
        return mark_safe(f"<span>{'<BR>'.join(describe)}</spam>")

    @display(description='IP')
    def show_ips(self, obj):
        return mark_safe('<BR>'.join(str(ip) for ip in obj.server.ip_addresses.all()))

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
