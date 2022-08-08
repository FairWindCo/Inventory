from django.contrib import admin
from django.contrib.admin import display

from info.models.applications import ApplicationServersSpecification


class ApplicationAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('name', 'external')
    fields = ['name', 'description', 'url', 'responsible', 'depends', 'external']
    autocomplete_fields = ('responsible', 'depends',)
    filter_horizontal = ('responsible', 'depends',)
    save_as = True


class ServerResponseAdmin(admin.TabularInline):
    list_display = (
        'display_role', 'display_response',
        'display_note')
    autocomplete_fields = ('role', 'response', 'response_person')
    model = ApplicationServersSpecification
    extra = 1

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


class ApplicationServerAdmin(admin.ModelAdmin):
    search_fields = ('application__name', 'server__name')
    list_display = ('display_application', 'display_server',
                    # 'display_role', 'display_response',
                    'display_note')
    list_filter = ('application__name',)
    autocomplete_fields = ('application', 'server')
    inlines = [ServerResponseAdmin]
    save_as = True

    @display(description='Сервер')
    def display_server(self, obj):
        return obj.server.name

    @display(description='Додаток')
    def display_application(self, obj):
        return obj.application.name

    # @display(description='Роль')
    # def display_role(self, obj):
    #     return obj.role.name if obj.role else '-'
    #
    # @display(description='Ответственность')
    # def display_response(self, obj):
    #     return obj.response.name if obj.response else '-'

    @display(description='Примітка')
    def display_note(self, obj):
        if len(obj.description) > 40:
            return f'{obj.description[:40]}...'
        else:
            return obj.description
