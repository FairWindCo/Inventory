import json

from django.db import models

from sysinfo.admin import CustomPageModelAdmin
from sysinfo.models import CustomModelPage


class JsonInfoReport(CustomModelPage):
    title = 'Завантажити звіт'  # set page title

    # Define some fields.
    my_field = models.FileField('Інформація від сервера')
    # my_relation = models.ForeignKey(MyChildModel1, null=True)

    help_text = 'Спеціальна форма для передачі інформації від автоматизованої утиліти'
    form_help_text = 'Форма для передачі файлу з конфігурацією серверу від автоматизованної утиліти'
    tooltip = 'Передача фалів з конфінами знятими з серверами'


    bound_admin = CustomPageModelAdmin

    def save(self):
        ...  # Implement data handling from self attributes here.

        # self.bound_admin has some useful methods.
        # self.bound_request allows you to access current HTTP request.
        try:
            with self.my_field.open("rt") as file:
                json_data = file.read()
                if json_data:
                    print(json_data)
                    from task_logger.views import process_host_system_info_json
                    report = process_host_system_info_json(json.loads(json_data))
                    self.bound_admin.message_success(self.bound_request, report.content.decode())
                else:
                    self.bound_admin.message_error(self.bound_request, "Немає данних")
        except Exception as e:
            self.bound_admin.message_error(self.bound_request, e)
