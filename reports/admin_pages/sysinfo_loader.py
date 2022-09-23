import json

from django.db import models

from sysinfo.admin import CustomPageModelAdmin
from sysinfo.models import CustomModelPage



class JsonInfoReport(CustomModelPage):
    title = 'Завантажити звіт'  # set page title

    # Define some fields.
    my_field = models.FileField('Інформація від сервера')
    # my_relation = models.ForeignKey(MyChildModel1, null=True)

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
                    from task_logger.views import process_json_info
                    report = process_json_info(json.loads(json_data))
                    self.bound_admin.message_success(self.bound_request, report.content.decode())
                else:
                    self.bound_admin.message_error(self.bound_request, "Немає данних")
        except Exception as e:
            self.bound_admin.message_error(self.bound_request, e)


