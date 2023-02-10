from django.db import models


# Create your models here.
from info.models import Server


class ServerTaskReport(models.Model):
    server = models.ForeignKey(Server, verbose_name='Сервер', on_delete=models.PROTECT,
                               related_name="reports", blank=True, null=True)
    report_date = models.DateTimeField(verbose_name='Час', blank=True, null=True)
    info = models.CharField(max_length=250, verbose_name='Інформація')
    is_error = models.BooleanField(verbose_name='Помилка', default=False)

    help_text = 'Журнал зі звітами від автоматичних тасків (скриптів), що працюють на серверах'
    form_help_text = 'Один записк про таск або скрипт, що відпрацював'
    tooltip = 'Журнал проботи автоматичних тасків та скриптів по серверам'

    class Meta:
        verbose_name = 'Журнал автоматичних тасків'
        verbose_name_plural = 'Журнал автоматичних тасків'
        app_label = 'logview'
        db_table = 'task_logger_servertaskreport'
