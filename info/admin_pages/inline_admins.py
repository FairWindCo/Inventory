from nested_admin.nested import NestedTabularInline

from info.models.applications import ApplicationServersSpecification, ApplicationServers


class ServerRoleSpecificationInlineAdmin(NestedTabularInline):
    model = ApplicationServersSpecification
    extra = 0


class ServerSpecificationInlineAdmin(NestedTabularInline):
    model = ApplicationServers
    extra = 0
    inlines = [ServerRoleSpecificationInlineAdmin]

