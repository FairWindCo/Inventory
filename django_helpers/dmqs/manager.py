from django.db.models import Manager

from django_helpers.dmqs.queryset import MemoryQuerySet
from django_helpers.dmqs.repository import Repository

repository = Repository()


class MemoryManager(Manager):
    def __init__(self, model, default_filters=None, lazy_filter=None):
        self.model_name =model.__name__ if hasattr(model, "__name__") else model.__class__.__name__
        self.model = model
        self.default_filters = default_filters
        self.lazy_filter = lazy_filter

    def get_queryset(self):
        return self.get_query_set()

    def get_query_set(self):
        """Returns a new QuerySet object.  Subclasses can override this method
        to easily customize the behavior of the Manager.
        """
        if self.lazy_filter:
            lazy_model = self.lazy_filter['_class']
            filter_name = "%s__id" % (self.lazy_filter['filter_field_name'])
            filter_val = self.lazy_filter['_filter']
            data_field_name = self.lazy_filter['data_field_name']
            return MemoryQuerySet(self.model, data=MemoryQuerySet(lazy_model,
                                                                  data=repository. \
                                                                  get_models(lazy_model)
                                                                  ).filter(**{filter_name: filter_val}
                                                                           ).values_list(data_field_name,
                                                                                         flat=True).data)

        if self.model_name in repository.get_names():
            if self.default_filters:
                return MemoryQuerySet(self.model,
                                      data=repository. \
                                      get_models(self.model_name)
                                      ).filter(**self.default_filters)
            else:
                return MemoryQuerySet(self.model,
                                      data=repository.get_models(self.model_name))
        elif hasattr(self.model, 'get_virtual_dataset'):
            data = self.model.get_virtual_dataset()
            if data:
                repository.insert_all(self.model_name, data)
                return MemoryQuerySet(self.model,
                                      data=repository.get_models(self.model_name))
        return MemoryQuerySet(self.model)

    def create(self, *args, **kwargs):
        return self.model(**kwargs).save()

    def _insert(self, *args, **kwargs):
        self.add(args[0][0])
    def add(self, instance):
        repository.save(self.model_name, instance)

    def __len__(self):
        return len(self.get_query_set().data)
