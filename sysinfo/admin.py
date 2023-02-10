from functools import update_wrapper
from typing import List

from django.contrib import messages, admin
from django.contrib.admin.decorators import register
from django.core.exceptions import PermissionDenied
from django.db import models
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path

from django_helpers.admin.utility_classes import MyCl

if False:  # pragma: nocover
    from .models import CustomModelPage  # noqa


class EtcAdmin(admin.ModelAdmin):
    """Base etc admin."""

    def message_success(self, request: HttpRequest, msg: str):
        self.message_user(request, msg, messages.SUCCESS)

    def message_warning(self, request: HttpRequest, msg: str):
        self.message_user(request, msg, messages.WARNING)

    def message_error(self, request: HttpRequest, msg: str):
        self.message_user(request, msg, messages.ERROR)


class ReadonlyAdmin(EtcAdmin):
    """Read-only etc admin base class."""

    view_on_site: bool = False
    actions = None

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: models.Model = None) -> bool:
        return False

    def changeform_view(
            self,
            request: HttpRequest,
            object_id: int = None,
            form_url: str = '',
            extra_context: dict = None
    ) -> HttpResponse:
        extra_context = extra_context or {}
        extra_context.update({
            'show_save_and_continue': False,
            'show_save': False,
        })
        return super().changeform_view(request, object_id, extra_context=extra_context)


class CustomPageModelAdmin(ReadonlyAdmin):
    """Base for admin pages with contents based on custom models."""

    def get_urls(self) -> list:
        meta = self.model._meta
        patterns = [path(
            '',
            self.admin_site.admin_view(self.view_custom),
            name=f'{meta.app_label}_{meta.model_name}_changelist'
        )]
        return patterns

    def has_add_permission(self, request: HttpRequest) -> bool:
        return True

    def view_custom(self, request: HttpRequest) -> HttpResponse:
        context: dict = {
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'title': self.model._meta.verbose_name,
        }
        return self._changeform_view(request, object_id=None, form_url='', extra_context=context)

    def response_add(self, request: HttpRequest, obj: 'CustomModelPage', post_url_continue=None):
        return HttpResponseRedirect(request.path)

    def save_model(self, request: HttpRequest, obj: 'CustomModelPage', form, change):
        obj.bound_request = request
        obj.bound_admin = self
        obj.save()


def custom_view(function=None, *, permissions=None, description=None, switch_field=None):
    def decorator(func):
        if permissions is not None:
            func.allowed_permissions = permissions
        if description is not None:
            func.short_description = description
            if isinstance(description, dict):
                assert switch_field, 'switch_field argument is required'
                func.switch_field = switch_field
        return func

    if function is None:
        return decorator
    else:
        return decorator(function)


class ViewsModelAdmin(EtcAdmin):
    change_views: List = ()
    list_views: List = ()

    def get_urls(self):
        urls = super(ViewsModelAdmin, self).get_urls()
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        for view, name, _ in self.get_extra_views(self.change_views):
            urls.append(
                path(f'<path:pk>/{name}', self.custom_admin_view(view), name=f'{app_label}_{model_name}_{name}')
            )
        for view, name, _ in self.get_extra_views(self.list_views):
            urls.insert(
                0,
                path(f'{name}/', self.custom_admin_view(view), name=f'{app_label}_{model_name}_{name}')
            )
        return urls

    def changelist_view(self, request, **kwargs):
        extra_context = {'extra_views': self.get_extra_views(self.list_views, request)}
        return super(ViewsModelAdmin, self).changelist_view(request, extra_context=extra_context, **kwargs)

    def change_view(self, request, object_id=None, **kwargs):
        extra_context = {'extra_views': self.get_extra_views(self.change_views, request)}
        return super(ViewsModelAdmin, self).changeform_view(request, object_id, extra_context=extra_context,
                                                            **kwargs)

    def get_extra_views(self, views, request=None):
        for view_name in views:
            view = self.get_view(view_name)
            if request and not self.has_permissions(request, view[0]):
                continue
            yield view

    def get_view(self, view):
        if callable(view):
            view_name = view.__name__
            func = view
        else:
            func = getattr(self, view)
            view_name = view

        description = getattr(func, 'short_description', view_name.replace('_', ' ').title())
        if isinstance(description, dict):
            description['switch_field'] = func.switch_field
        return func, view_name, description

    def get_context(self, request, title):
        opts = self.model._meta
        return {
            **self.admin_site.each_context(request),
            'title': title,
            'module_name': str(opts.verbose_name_plural),
            'opts': opts,
            'preserved_filters': self.get_preserved_filters(request),
        }

    def has_permissions(self, request, view):
        check = []
        allowed_permissions = getattr(view, 'allowed_permissions', [])
        for allowed_permission in allowed_permissions:
            has_permission = getattr(self, f'has_{allowed_permission}_permission')
            check.append(has_permission(request))
        return all(check)

    def custom_admin_view(self, custom_view):
        admin_view = self.admin_site.admin_view(custom_view)

        def wrap(view, cacheable=False):
            def wrapper(request, *args, **kwargs):
                if not self.has_permissions(request, view):
                    raise PermissionDenied
                return self.admin_site.admin_view(view, cacheable)(request, *args, **kwargs)

            return update_wrapper(wrapper, view)

        return wrap(admin_view)

    @staticmethod
    def has_superuser_permission(request):
        return request.user.is_superuser

    @classmethod
    def register(cls, *, modelclass=None):
        if modelclass is None:
            from .models import CustomModelPage  # noqa
            new_class_name = cls.__name__ + 'Model'
            meta = type('Meta', (object,), {
                'managed': False
            })
            modelclass = type(new_class_name, (CustomModelPage,), {
                '__module__': cls.__module__,
                # 'Meta': meta
            })
            # modelclass.__module__ = cls.__module__
        register(modelclass)(cls)


class CustomViewsModelAdmin(ViewsModelAdmin):
    view_title = 'Custom View Title'

    def changelist_view(self, request, **kwargs):
        opts = self.model._meta
        app_label = self.view_title
        extra_context = {'extra_views': self.get_extra_views(self.list_views, request)}
        cl = MyCl(self.view_title)
        context = {
            **self.admin_site.each_context(request),
            'module_name': '',
            'selection_note': '',  # _('0 of %(cnt)s selected') % {'cnt': len(cl.result_list)},
            'selection_note_all': 0,  # selection_note_all % {'total_count': cl.result_count},
            'title': self.view_title,
            'subtitle': None,
            'is_popup': 'cl.is_popup',
            'to_field': 'cl.to_field',
            'cl': cl,
            'media': 'media',
            'has_add_permission': self.has_add_permission(request),
            'opts': cl.opts,
            'action_form': 'action_form',
            'actions_on_top': self.actions_on_top,
            'actions_on_bottom': self.actions_on_bottom,
            'actions_selection_counter': self.actions_selection_counter,
            'preserved_filters': self.get_preserved_filters(request),
            **(extra_context or {}),
        }

        request.current_app = self.admin_site.name

        return TemplateResponse(request, self.change_list_template or [
            'admin/%s/%s/change_list.html' % (app_label, opts.model_name),
            'admin/%s/change_list.html' % app_label,
            'admin/change_list.html'
        ], context)
