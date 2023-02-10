class MyOpts:
    def __init__(self, title, app_label='admin', app_config=None):
        self.app_label = app_label
        self.app_config = app_config if app_config is not None else MyAppConfig(title)
        self.object_name = title
        self.verbose_name = title
        self.model_name = title


class MyCl:
    def __init__(self, title, opts=None, **kwarg):
        self.opts = opts if opts is not None else MyOpts(title)
        self.result_count = 10
        self.full_result_count = 100
        self.list_display = ('id', 'name')
        self.formset = ()
        self.result_list = ()
        self.show_all = True
        self.can_show_all = True
        self.model = {
            '_meta': {
                'name': title
            }
        }
        self.model_admin = {
            '_meta': {
                'name': title
            }
        }
        for k, v in kwarg.items():
            setattr(self, k, v)

    def get_result_list(self):
        return ({'id': i,
                 'name': 'test ' + i} for i in range(self.result_count))

    def get_ordering_field_columns(self):
        return None


class MyAppConfig:
    def __init__(self, verbose_name):
        self.verbose_name = verbose_name
