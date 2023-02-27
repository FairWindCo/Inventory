from django.contrib import admin
from django.db.models import CharField

from django_helpers.admin import CustomModelPage
from django_helpers.admin.custom_admin_page import CustomizeAdmin, CustomDBModelPage
from django_helpers.admin.custom_change_list import CustomAdminPagePrototype
from django_helpers.dmqs.memory_model import CustomMemoryModel
# Register your models here.
from reports.admin_pages.applications import AppInfoAdminProxy, ApplicationServerInfoAdmin, AppInfoAProxy, \
    ApplicationInfoAdmin
from reports.admin_pages.futures_service import FutureAdminProxy, SoftFutureAdmin, DaemonsAdminProxy, DaemonsAdmin, \
    ServerTaskAdminProxy, ServerTaskAdmin
from reports.admin_pages.ip_adress import IPProxy, IPNetworkReport
from reports.admin_pages.server_response import SpecificationProxy, ResponseInfoAdmin
from reports.admin_pages.servers import ServerInfoAdminProxy, ServerInfoViewAdmin
from reports.admin_pages.servers_infos import ApplicationServersSpecificationProxy
from reports.admin_pages.softs import SoftInfoAdminProxy, SoftInfoAdmin, InstalledSoftInfoAdmin, \
    InstalledSoftInfoAdminProxy
from reports.admin_pages.sysinfo_loader import JsonInfoReport
from reports.admin_pages.update_status import ServerAdminProxy, ServerViewAdmin
from sysinfo.admin import ViewsModelAdmin, CustomViewsModelAdmin

admin.site.register(ServerAdminProxy, ServerViewAdmin)
admin.site.register(ServerInfoAdminProxy, ServerInfoViewAdmin)
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
        return [{'pk':1},{'pk':2},{'pk':3},{'pk':4}]




class MyCustomModelPage(CustomModelPage):
    pass

class MyCustomDBModelPage(CustomMemoryModel):
    name = CharField(max_length=100)

class MyCustomAdminPage(CustomAdminPagePrototype):
    app_label: str = 'admin'

#CustomViewsModelAdmin.register()
##MyCustomModelPage.register()
#MyCustomDBModelPage.register()
#MyCustomAdminPage.register()
