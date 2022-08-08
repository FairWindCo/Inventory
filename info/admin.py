from django.contrib import admin

from dictionary.admin import SimpleNameAdmin
from dictionary.models import ServerScheduledTask
from .admin_pages.application_admin import ApplicationAdmin, ApplicationServerAdmin
from .admin_pages.configuration_admin import ConfigurationServerAdmin, DiskAdmin
from .admin_pages.server_admin import ServerAdmin
from .admin_pages.soft_installed_admin import HostInstalledSoftwareAdmin, HostScheduledTaskAdmin
from .models import *
# In models.py
from .models.applications import ApplicationServers, HostScheduledTask

# Register your models here.

admin.site.register(Application, ApplicationAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(ResponsiblePerson, SimpleNameAdmin)
admin.site.register(HostInstalledSoftware, HostInstalledSoftwareAdmin)
admin.site.register(HostScheduledTask, HostScheduledTaskAdmin)
admin.site.register(ApplicationServers, ApplicationServerAdmin)
admin.site.register(Configuration, ConfigurationServerAdmin)
admin.site.register(DiskConfiguration, DiskAdmin)