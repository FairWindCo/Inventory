from django.contrib import admin
from django.contrib.admin import display

from info.models.applications import ApplicationServersSpecification


class ApplicationServersSpecificationProxy(ApplicationServersSpecification):
    class Meta:
        proxy = True
        verbose_name = 'Призначення сервера'
        verbose_name_plural = 'Призначення серверів'


class ServerResponseInfoAdmin(admin.TabularInline):
    list_display = (
        'display_role', 'display_response',
        'display_note')
    autocomplete_fields = ('role', 'response', 'response_person')
    model = ApplicationServersSpecificationProxy
    extra = 0

    @display(description='Відповідальність')
    def display_response(self, obj):
        return obj.response.name if obj.response else '-'

    @display(description='Примітка')
    def display_note(self, obj):
        if len(obj.description) > 40:
            return f'{obj.description[:40]}...'
        else:
            return obj.description

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
