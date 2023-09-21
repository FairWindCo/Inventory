import json

from django.contrib import admin
from django.db import models
from django.db.models import CharField
from django.http import HttpRequest
from django.utils.safestring import mark_safe

from dictionary.models import OS
from django_helpers.admin import CustomModelPage
from django_helpers.admin.change_title_admin import ChangeTitleAdminModel
from django_helpers.admin.custom_admin_page import CustomizeAdmin
from django_helpers.admin.custom_change_list import CustomAdminPagePrototype
from django_helpers.dmqs.memory_model import CustomMemoryModel
from info.models import Server
# Register your models here.
from reports.admin_pages.applications import AppInfoAdminProxy, ApplicationServerInfoAdmin, AppInfoAProxy, \
    ApplicationInfoAdmin
from reports.admin_pages.futures_service import FutureAdminProxy, SoftFutureAdmin, DaemonsAdminProxy, DaemonsAdmin, \
    ServerTaskAdminProxy, ServerTaskAdmin
from reports.admin_pages.hardware_report import ServerHardwareInfoAdminProxy, HardwareInfoViewAdmin
from reports.admin_pages.ip_adress import IPProxy, IPNetworkReport
from reports.admin_pages.server_response import SpecificationProxy, ResponseInfoAdmin
from reports.admin_pages.servers import ServerInfoAdminProxy, ServerInfoViewAdmin
from reports.admin_pages.softs import SoftInfoAdminProxy, SoftInfoAdmin, InstalledSoftInfoAdmin, \
    InstalledSoftInfoAdminProxy
from reports.admin_pages.sysinfo_loader import JsonInfoReport
from reports.admin_pages.update_status import ServerAdminProxy, ServerViewAdmin

admin.site.register(ServerAdminProxy, ServerViewAdmin)
admin.site.register(ServerInfoAdminProxy, ServerInfoViewAdmin)
admin.site.register(ServerHardwareInfoAdminProxy, HardwareInfoViewAdmin)
admin.site.register(AppInfoAdminProxy, ApplicationServerInfoAdmin)
admin.site.register(AppInfoAProxy, ApplicationInfoAdmin)
admin.site.register(SoftInfoAdminProxy, SoftInfoAdmin)
admin.site.register(InstalledSoftInfoAdminProxy, InstalledSoftInfoAdmin)
admin.site.register(SpecificationProxy, ResponseInfoAdmin)
admin.site.register(FutureAdminProxy, SoftFutureAdmin)
admin.site.register(DaemonsAdminProxy, DaemonsAdmin)
admin.site.register(ServerTaskAdminProxy, ServerTaskAdmin)
admin.site.register(IPProxy, IPNetworkReport)

JsonInfoReport.register()


class Test(CustomizeAdmin):
    #  custom_list_view = "True"
    @staticmethod
    def get_virtual_dataset():
        return [{'pk': 1}, {'pk': 2}, {'pk': 3}, {'pk': 4}]


class OSStateReports(CustomizeAdmin, ChangeTitleAdminModel):
    title = 'Звіт про стан ОС'
    app_label: str = 'reports'
    model_title = 'Звіт про стан ОС'

    help_text = 'Діаграми про стан ОС'
    form_help_text = 'Інформаційний звіт про стан ОС'
    tooltip = 'Звіт про стан ОС'

    list_template = 'django_helpers/custom_chart.html'

    def custom_list_view(self, requests):
        os_dict = {}
        famali_dict = {}
        old_system_count = 0
        system_count = 0
        for os in OS.objects.all():
            count_servers = os.server_set.exclude(status__in=[Server.ServerState.DELETED]).count()
            if count_servers > 0:
                os_dict[os.name] = count_servers
                famali_name = os.family if os.family else 'Інше'
                famali_dict[famali_name] = famali_dict.get(famali_name, 0) + count_servers
                if os.old:
                    old_system_count += count_servers
                else:
                    system_count += count_servers
        if os_dict:
            config1 = {
                'type': 'pie',
                'data': {
                    'labels': list(os_dict.keys()),
                    'datasets': [{
                        'label': 'Операційних систем',
                        # 'data': [{'label': key, 'value': value} for key, value in os_dict.items()]
                        'data': list(os_dict.values())
                    }]
                },
                'options': {
                    'responsive': True,
                    'plugins': {
                        'legend': {
                            'display': False,
                            'position': 'top',
                        },
                        'title': {
                            'display': True,
                            'text': 'Розподіл хостів за ОС'
                        },
                    },
                    'layout': {
                        'padding': 20
                    },
                },
            }
            config2 = {
                'type': 'pie',
                'data': {
                    'labels': list(famali_dict.keys()),
                    'datasets': [{
                        'label': 'Операційних систем',
                        # 'data': [{'label': key, 'value': value} for key, value in os_dict.items()]
                        'data': list(famali_dict.values())
                    }]
                },
                'options': {
                    'responsive': True,
                    'plugins': {
                        'legend': {
                            'display': False,
                            'position': 'top',
                        },
                        'title': {
                            'display': True,
                            'text': 'Розподіл ОС за родами'
                        },
                    },
                    'layout': {
                        'padding': 20
                    },
                },
            }
            config3 = {
                'type': 'pie',
                'data': {
                    'labels': ['Застарілі', 'Нормальні'],
                    'datasets': [{
                        'label': 'Операційних систем',
                        # 'data': [{'label': key, 'value': value} for key, value in os_dict.items()]
                        'data': [old_system_count, system_count],
                        'backgroundColor': [
                            'rgb(255, 99, 132)',
                            'rgb(54, 162, 235)',
                            'rgb(255, 205, 86)'
                        ],
                    }]
                },
                'options': {
                    'responsive': True,
                    'plugins': {
                        'legend': {
                            'display': False,
                            'position': 'top',
                        },
                        'title': {
                            'display': True,
                            'text': 'Розподіл за віком'
                        },
                    },
                    'layout': {
                        'padding': 20
                    },
                },
            }
            HTML = '''
                <div style="display:flex;flex-direction: row;flex-wrap: wrap;">
                    <div style="flex-grow: 1;width:600px;"><canvas id="chart1"></canvas></div>
                    <div style="flex-grow: 1;width:600px;"><canvas id="chart2"></canvas></div>
                    <div style="flex-grow: 1;width:600px;"><canvas id="chart3"></canvas></div>
                </div>
                <script>
            const ctx1 = document.getElementById('chart1');
            const ctx2 = document.getElementById('chart2');
            const ctx3 = document.getElementById('chart3');
            new Chart(ctx1, %s);
            new Chart(ctx2, %s);
            new Chart(ctx3, %s);
            </script>
            ''' % (json.dumps(config1), json.dumps(config2), json.dumps(config3))
        else:
            HTML = "Немає відповідних серверів"
        return mark_safe(HTML)

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: models.Model = None) -> bool:
        return False

    def has_change_permission(self, request, obj=None):
        return False


class MyCustomModelPage(CustomModelPage):
    pass


class MyCustomDBModelPage(CustomMemoryModel):
    name = CharField(max_length=100)


class MyCustomAdminPage(CustomAdminPagePrototype):
    app_label: str = 'admin'


# CustomViewsModelAdmin.register()
# MyCustomModelPage.register()
# MyCustomDBModelPage.register()
# MyCustomAdminPage.register()
OSStateReports.register()
