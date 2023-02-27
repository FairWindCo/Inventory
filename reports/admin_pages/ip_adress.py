import ipaddress
from functools import update_wrapper

from django.contrib import admin
from django.contrib.admin import display
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from dictionary.models import IP
from django_helpers.admin.change_title_admin import ChangeTitleAdminModel
from info.models import Server


class IPProxy(IP):
    help_text = 'Перелік ІР адрес які використовується в нашій системі'
    tooltip = 'Перелік ІР, що використовується в системі'

    class Meta:
        proxy = True
        verbose_name = 'IP та мережі'
        verbose_name_plural = 'IP та мережі'


# @admin.register(IPProxy)
class IPNetworkReport(ChangeTitleAdminModel):
    list_display = ('show_action', 'ip_address', 'mask', 'show_room', 'comment')
    list_filter = ('room',)

    def get_queryset(self, request):
        qs = IPProxy.objects.filter(mask__lt=32)
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    @display(description="Серверна")
    def show_room(self, obj):
        return obj.room.first().name if obj.room and obj.room.first() else None

    @display(description="Дія")
    def show_action(self, obj):
        info = self.model._meta.app_label, self.model._meta.model_name

        return mark_safe("".join([
            f"<a href={reverse('admin:%s_%s_free' % info, args=(obj.pk,))} class='btn btn-primary'>Вільні</a>",
            f"<a href={reverse('admin:%s_%s_use' % info, args=(obj.pk,))} class='btn btn-primary'>Використовуються</a>",
        ]))

    def render_ip_list(self, request, ip_list, title, subtitle='', comments='', headers=None, current_id=None):
        if headers is None:
            headers = ({'text': 'IP'}, {'text': 'Примітка'},)
        return TemplateResponse(
            request,
            template='admin/ip_list.html',
            context={
                **self.admin_site.each_context(request),
                'opts': self.opts, 'cl': self,
                'results': ip_list,
                'title': title,
                'subtitle': subtitle,
                'comment': comments,
                'result_headers': headers,
                'current_id': current_id,
            }
        )

    def render_ip_list_detail(self, request, ip_list, title, subtitle='', comments='', headers=None, current_id=None):
        if headers is None:
            headers = ({'text': 'IP'}, {'text': 'Сервер'}, {'text': 'Примітка'},)
        return self.render_ip_list(request, ip_list, title, subtitle, comments, headers, current_id)

    @staticmethod
    def get_ip(object_id):
        ipnet = IPProxy.objects.get(id=object_id)
        network_name = f'{ipnet.ip_address}/{ipnet.mask}'
        return ipnet, ipaddress.ip_network(network_name, False), network_name

    @staticmethod
    def find_sub_host(ipnet, filter=lambda a: a):
        base_mask = ipnet.mask // 8
        global_network_name = f'{ipnet.ip_address}/{base_mask * 8}'
        net_mask = ipaddress.ip_network(global_network_name, False)
        sub_mak = str(net_mask.network_address)[:-2 * (4 - base_mask)]
        return filter(IPProxy.objects.order_by('ip_address').
                      filter(ip_address__startswith=sub_mak, mask__gt=ipnet.mask)).distinct()

    def find_sub_host_by_network_id(self, object_id, filter=lambda a: a):
        ipnet, ipobj, network_name = self.get_ip(object_id)
        sub_hosts = self.find_sub_host(ipnet, filter)
        return ipnet, ipobj, network_name, sub_hosts

    def render_detail_view(self, request, object_id, title, filter=lambda a: a):
        ipnet, ipobj, network_name, sub_hosts = self.find_sub_host_by_network_id(object_id, filter)
        hosts = list(map(lambda ip: (ip.ip_address, ip.get_server_names(), ip.comment), sub_hosts))
        return self.render_ip_list_detail(request, hosts, title, f'Мережа: {network_name}', ipnet.comment,
                                          current_id=object_id)

    def use_view(self, request, object_id, form_url="", extra_context=None):
        return self.render_detail_view(request, object_id, 'Адреси у використанні',
                                       lambda a: a.exclude(servers__status__in=[Server.ServerState.DELETED]))

    def register_view(self, request, object_id, form_url="", extra_context=None):
        return self.render_detail_view(request, object_id, 'Зареєстровані адреси мережі')

    def exlude_view(self, request, object_id, title, filter=lambda a: a):
        ipnet, ipobj, network_name, sub_hosts = self.find_sub_host_by_network_id(object_id, filter)
        host_exlide_list = list([ip.ip_address for ip in sub_hosts])
        hosts = [(host, '') for host in ipobj.hosts()
                 if not str(host) in host_exlide_list]
        #hosts = []
        # for host in ipobj.hosts():
        #     ip_text = str(host)
        #     if not ip_text in host_exlide_list:
        #         hosts.append((host, ''))
        return self.render_ip_list(request, hosts, title, f'Мережа: {network_name}',
                                   ipnet.comment, current_id=object_id)

    def free_view(self, request, object_id, form_url="", extra_context=None):
        return self.exlude_view(request, object_id, 'Вільні адреси',
                                lambda a: a.exclude(servers__status__in=[Server.ServerState.DELETED]))

    def untoched_view(self, request, object_id, form_url="", extra_context=None):
        return self.exlude_view(request, object_id, 'Адреси, що ніколи не використовувалися')

    def change_view(self, request, object_id, form_url="", extra_context=None):
        ipnet, ipobj, network_name = self.get_ip(object_id)
        hosts = list(map(lambda i: (str(i), ''), ipobj.hosts()))
        return self.render_ip_list(request, hosts, 'Повний перелік адрес мережі', f'Мережа: {network_name}',
                                   ipnet.comment)

    def changelist_view(self, request, extra_context=None):
        return super().changelist_view(request, extra_context)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_urls(self):
        from django.urls import path

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        return [
            path("", wrap(self.changelist_view), name="%s_%s_changelist" % info),
            path(
                "<path:object_id>/full_list/",
                wrap(self.change_view),
                name="%s_%s_full_list" % info,
            ),
            path(
                "<path:object_id>/registered/",
                wrap(self.register_view),
                name="%s_%s_registered" % info,
            ),
            path(
                "<path:object_id>/use/",
                wrap(self.use_view),
                name="%s_%s_use" % info,
            ),
            path(
                "<path:object_id>/free/",
                wrap(self.free_view),
                name="%s_%s_free" % info,
            ),
            path(
                "<path:object_id>/not_init/",
                wrap(self.untoched_view),
                name="%s_%s_not_init" % info,
            ),

        ]
