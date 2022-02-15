from django.contrib import admin


class ApplicationAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('name',)
    fields = ['name', 'description', 'url', 'responsible']
    autocomplete_fields = ('responsible',)
    filter_horizontal = ('responsible',)


class ApplicationServerAdmin(admin.ModelAdmin):
    search_fields = ('application__name', 'server__name')
    # list_filter = ('name',)
    autocomplete_fields = ('application', 'server', 'role', 'response')
