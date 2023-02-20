from django.contrib import admin

from info.models.applications import ApplicationServersSpecification, ApplicationServers


class ServerSpecificationInlineAdmin(admin.TabularInline):
    model = ApplicationServers
    extra = 0

