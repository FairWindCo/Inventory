from django.contrib import admin
from django.contrib.admin import display

from info.models.applications import ApplicationServersSpecification


class SpecificationProxy(ApplicationServersSpecification):
    class Meta:
        proxy = True
        verbose_name = 'Призначення сервера'
        verbose_name_plural = 'Призначення серверів'


class ResponseInfoAdmin(admin.ModelAdmin):
    list_display = (
        'display_server', 'display_application',
        'display_role', 'display_response',
        'display_note')
    list_filter = ('role__name', 'response__name', 'application_server__application__name')
    search_fields = ('application_server__server__name', 'role__name',
                     'response__name', 'application_server__application__name')
    autocomplete_fields = ('role', 'response', 'response_person')

    @display(description='Сервер')
    def display_server(self, obj):
        return obj.application_server.server.name if obj.application_server else '-'

    @display(description='Додаток')
    def display_application(self, obj):
        return obj.application_server.application.name if obj.application_server else '-'

    @display(description='Роль')
    def display_role(self, obj):
        return obj.role.name if obj.role else '-'

    @display(description='Відповідальність')
    def display_response(self, obj):
        return obj.response.name if obj.response else '-'

    @display(description='Примітка')
    def display_note(self, obj):
        if len(obj.description) > 40:
            return f'{obj.description[:40]}...'
        else:
            return obj.description

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
