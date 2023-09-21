from typing import Optional

import django
from django.db import models
from django.db.models.options import Options

from django_helpers.dmqs.manager import MemoryManager

if django.get_version().startswith('4'):
    from django.urls import re_path as url
else:
    from django.conf.urls import url

from django.http import HttpResponseRedirect, HttpRequest
from django.template.response import TemplateResponse
from django.urls import reverse
from django.contrib.admin.decorators import register

from django_helpers.admin import SelfRegisterAdmin, wrap
from django_helpers.admin.utility_classes import MyCl
from django.utils.translation import gettext_lazy as _


# Класс для переопределения стандартных URL для админки
# Имеет встроенное поле redefined_urls словарь:
# шаблон -> (view, name_for_reverse)
class RedefineUrlAdmin(SelfRegisterAdmin):
    redefined_urls = {}

    def get_urls(self):
        urlpatterns = []
        for pattern, value in self.redefined_urls.items():
            urlpatterns += [url(pattern, wrap(value[0], self), name=value[1])]
        urlpatterns += super().get_urls()
        return urlpatterns


class CustomizeAdmin(SelfRegisterAdmin):
    title = 'wizard'

    result_chane_url = 'admin:%s_%s_changelist'
    result_add_url = 'admin:%s_%s_changelist'
    result_delete_url = 'admin:%s_%s_changelist'
    # this is method or value that use for render list page
    custom_list_view = None
    # this is method or value that use for render change object page
    custom_change_view = None
    # this is method or value that use for render delete object page
    custom_delete_view = None
    # this is method or value that use for render add object page
    custom_add_view = None
    # this is template for render change/add form
    form_template = 'django_helpers/custom_page.html'
    # this is template for render list page
    list_template = 'django_helpers/custom_page.html'

    # convert view to string (render view)
    def render_view_to_str(self, view, request, object_id=None, **extra_context):
        if view is None:
            return None
        if isinstance(view, type):
            return view.as_view()(request, object_id, **extra_context)
        elif callable(view):
            return view(request)
        else:
            return view

    # form response
    def custom_view_response(self, request, rendered_view, result_url, template, extra_context: dict = None):
        if extra_context is None:
            extra_context = {}
        if rendered_view is None:
            return HttpResponseRedirect(
                reverse(result_url % (self.model._meta.app_label, self.model._meta.model_name)))

        render_str = rendered_view.rendered_content if hasattr(rendered_view, 'rendered_content') else rendered_view
        cl = MyCl('test')
        context = {**self.admin_site.each_context(request),
                   'title': self.title,
                   'preserved_filters': self.get_preserved_filters(request),
                   'app_label': 'admin', 'cl': cl,
                   'opts': cl.opts,
                   'view_extra': render_str}
        context.update(extra_context or {})

        return TemplateResponse(request, template, context)

    # method for customize add/chane view
    def custom_view_form_wrapper(self, request, object_id=None, extra_context: dict = None):
        if extra_context is None:
            extra_context = {}
        if object_id is None and self.custom_add_view is not None:
            rendered_view = self.render_view_to_str(self.custom_add_view, request, None, **extra_context)
            result_url = self.result_add_url
        else:
            rendered_view = self.render_view_to_str(self.custom_change_view, request, object_id, **extra_context)
            result_url = self.result_chane_url
        return self.custom_view_response(request, rendered_view, result_url, self.form_template, extra_context)

    # method for customize list view
    def custom_view_list_wrapper(self, request, extra_context: dict = None):
        if extra_context is None:
            extra_context = {}
        rendered_view = self.render_view_to_str(self.custom_list_view, request, **extra_context)
        result_url = self.result_chane_url
        return self.custom_view_response(request, rendered_view, result_url, self.list_template, extra_context)

    # overwrite changeform_view for add custom_change_view customizer
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if self.custom_change_view:
            return self.custom_view_form_wrapper(request, object_id, extra_context)
        return super().changeform_view(request, object_id, form_url, extra_context)

    # overwrite add_view for add custom_add_view customizer
    def add_view(self, request, form_url='', extra_context=None):
        if self.custom_add_view:
            return self.custom_view_form_wrapper(request, None, extra_context)
        return super().add_view(request, form_url, extra_context)

    # overwrite changelist_view for add custom_list_view customizer
    def changelist_view(self, request, extra_context=None):
        if self.custom_list_view:
            return self.custom_view_list_wrapper(request, extra_context)
        return super().changelist_view(request, extra_context)

    @staticmethod
    def get_virtual_dataset():
        return None

    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        manager = MemoryManager(self.model)
        qs = manager.get_query_set()
        # TODO: this should be handled by some parameter to the ChangeList.
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class MyMetaModel(django.db.models.base.ModelBase):
    @property
    def _base_manager(cls):
        return MemoryManager(cls)



class CustomDBModelPage(models.Model, metaclass=MyMetaModel):
    """Allows construction of admin_pages pages based on user input.
    Define your fields (as usual in models) and override .save() method.
    .. code-block:: python
        class MyPage(CustomModelPage):
            title = 'Test page 1'  # set page title
            # Define some fields.
            my_field = models.CharField('some title', max_length=10)
            def save(self):
                ...  # Implement data handling.
                super().save()
        # Register my page within Django admin_pages.
        MyPage.register()
    """
    title: str = _('Custom Model Admin page')
    """Page title to be used."""

    app_label: str = 'admin'
    """Application label to relate page to. Default: admin_pages"""

    bound_request: Optional[HttpRequest] = None
    """Request object bound to the model"""

    bound_admin: Optional[SelfRegisterAdmin] = None
    """Django admin_pages model bound to this model."""

    class Meta:
        abstract = True
        managed = False
        # base_manager_name = 'in_memory_manager'
        # proxy = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def __init_subclass__(cls) -> None:
        meta = cls.Meta
        meta.verbose_name = meta.verbose_name_plural = cls.title
        meta.app_label = cls.app_label
        super().__init_subclass__()


    @classmethod
    def register(cls, *, admin_model: CustomizeAdmin = None):
        """Registers this model page class in Django admin_pages.
        :param admin_model:
        """
        register(cls)(admin_model or CustomizeAdmin)

    # def save(self):  # noqa
    #     """Heirs should implement their own save handling."""
    #     if self.bound_admin:
    #         self.bound_admin.message_success(self.bound_request, _('Done.'))
