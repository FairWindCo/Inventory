from typing import Optional

from django.contrib.admin import ModelAdmin
from django.contrib.admin.decorators import register
from django.db.models.base import ModelBase, Model
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from django_helpers.dmqs.manager import MemoryManager


# Example in memory model (create a model
# class MyCustomDBModelPage(CustomMemoryModel):
#     name = CharField(max_length=100)
#
# MyCustomDBModelPage.register()

class MemoryMetaModel(ModelBase):
    @property
    def _base_manager(cls):
        return MemoryManager(cls)

    @property
    def _default_manager(cls):
        return MemoryManager(cls)


class CustomMemoryModel(Model, metaclass=MemoryMetaModel):
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

    bound_admin: Optional[ModelAdmin] = None
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
    def register(cls, *, admin_model: ModelAdmin = None):
        """Registers this model page class in Django admin_pages.
        :param admin_model:
        """
        register(cls)(admin_model or ModelAdmin)
