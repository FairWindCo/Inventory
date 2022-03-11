from django.contrib import admin

# Register your models here.
from reports.admin_pages.applications import AppInfoAdminProxy, ApplicationServerInfoAdmin, AppInfoAProxy, \
    ApplicationInfoAdmin
from reports.admin_pages.servers import ServerInfoAdminProxy, ServerInfoViewAdmin
from reports.admin_pages.server_response import SpecificationProxy, ResponseInfoAdmin
from reports.admin_pages.softs import SoftInfoAdminProxy, SoftInfoAdmin, InstalledSoftInfoAdmin, \
    InstalledSoftInfoAdminProxy
from reports.admin_pages.update_status import ServerAdminProxy, ServerViewAdmin

admin.site.register(ServerAdminProxy, ServerViewAdmin)
admin.site.register(ServerInfoAdminProxy, ServerInfoViewAdmin)
admin.site.register(AppInfoAdminProxy, ApplicationServerInfoAdmin)
admin.site.register(AppInfoAProxy, ApplicationInfoAdmin)
admin.site.register(SoftInfoAdminProxy, SoftInfoAdmin)
admin.site.register(InstalledSoftInfoAdminProxy, InstalledSoftInfoAdmin)
admin.site.register(SpecificationProxy, ResponseInfoAdmin)
