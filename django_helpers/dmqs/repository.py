from collections import defaultdict


def fetch_primary_key(model_instance):
    try:
        return getattr(model_instance, 'id')
    except:
        for field in model_instance._meta.fields:
            if field.primary_key:
                return getattr(model_instance, field.name)


class Repository(object):
    __shared_state = {}
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.__dict__ = self.__shared_state
        self.__dict__['data'] = defaultdict(list)
        self.__dict__['ids'] = defaultdict(int)

    def get_models(self, model_name):
        return self.__dict__['data'][model_name]

    def get_names(self):
        return self.__dict__['data'].keys()

    def clean(self):
        self.__dict__['data'] = defaultdict(list)

    def insert_all(self, model_name, values):
        self.__dict__['data'][model_name] = values

    def save(self, model_name, value):
        update = False

        for i, model in enumerate(self.get_models(model_name)):
            if fetch_primary_key(model) == fetch_primary_key(value):
                self.get_models(model_name)[i] = value
                update = True

        if not update:
            if fetch_primary_key(value) == None:
                self.__dict__['ids'][model_name] += 1
                value.id = self.__dict__['ids'][model_name]
            self.get_models(model_name).append(value)

        return update

    def delete(self, model_name, value):
        self.__dict__['data'][model_name][:] = \
            [x for x in self.__dict__['data'][model_name]
             if x not in value]