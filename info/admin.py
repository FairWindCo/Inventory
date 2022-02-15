from django.contrib import admin

from dictionary.admin import SimpleNameAdmin
from .admin_pages.application_admin import ApplicationAdmin, ApplicationServerAdmin
from .admin_pages.server_admin import ServerAdmin, ServerAdminProxy, ServerViewAdmin
from .admin_pages.soft_installed_admin import HostInstalledSoftwareAdmin
from .models import *

# Register your models here.


# In models.py
from .models.applications import ApplicationServers

admin.site.register(Application, ApplicationAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(ServerAdminProxy, ServerViewAdmin)
admin.site.register(ResponsiblePerson, SimpleNameAdmin)
admin.site.register(HostInstalledSoftware, HostInstalledSoftwareAdmin)
admin.site.register(ApplicationServers, ApplicationServerAdmin)
