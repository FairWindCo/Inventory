from django.contrib.admin import ModelAdmin


class ChangeTitleAdminModel(ModelAdmin):
    list_title_pattern = "{}"
    change_title_pattern = "{}"

    def get_changelist_instance(self, request):
        changelist_instance = super().get_changelist_instance(request)
        changelist_instance.title = self.list_title_pattern.format(changelist_instance.opts.verbose_name)
        return changelist_instance

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        context = super().changeform_view(request, object_id, form_url, extra_context)
        context['title'] = self.change_title_pattern.format(self.model._meta.verbose_name)
        return context
