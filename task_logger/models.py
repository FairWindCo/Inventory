from django.db import models

# Create your models here.
from info.models import Server


class ServerTaskReport(models.Model):
    server = models.ForeignKey(Server, verbose_name='Сервер', on_delete=models.PROTECT,
                               related_name="reports", blank=True, null=True)
    report_date = models.DateTimeField(verbose_name='Час', blank=True, null=True)
    info = models.CharField(max_length=250, verbose_name='Інформація')
    is_error = models.BooleanField(verbose_name='Помилка', default=False)
    code = models.CharField(max_length=50, verbose_name='Код задачі для контролю', blank=True, null=True, default=None)
    help_text = 'Журнал зі звітами від автоматичних тасків (скриптів), що працюють на серверах'
    form_help_text = 'Один записк про таск або скрипт, що відпрацював'
    tooltip = 'Журнал проботи автоматичних тасків та скриптів по серверам'

    class Meta:
        verbose_name = 'Журнал автоматичних тасків'
        verbose_name_plural = 'Журнал автоматичних тасків'
        app_label = 'logview'
        db_table = 'task_logger_servertaskreport'


class TaskControlGroup(models.Model):
    name = models.CharField(max_length=50, verbose_name='Назва групи')
    send_message = models.BooleanField(default=True, verbose_name='Формувати звіт про группу')

    def __str__(self):
        return f"{self.name if self.name else ''}"

    class Meta:
        verbose_name = 'Групи контролю автоматичних тасків'
        verbose_name_plural = 'Групи контролю автоматичних тасків'
        app_label = 'logview'
        db_table = 'task_logger_taskcontrolgroup'


class TaskControl(models.Model):
    DAY = 24 * 60 * 60
    HOUR = 60 * 60
    MINUTES = 60
    SECONDS = 1

    NOT_NOTYFY = 0
    TELGRRAM_NOTIFY = 1
    MAIL_NOTIFY = 1
    ALL_NOTIFY = 3

    NOTIFY = (
        (NOT_NOTYFY, 'Не сповіщати'),
        (TELGRRAM_NOTIFY, 'Сопвіщувати по телеграм'),
        (MAIL_NOTIFY, 'Сповіщувати поштою'),
        (ALL_NOTIFY, 'Всіма засобами сповіщення'),
    )

    INTERVALS = (
        (DAY, 'День'),
        (HOUR, 'Година'),
        (MINUTES, 'Хвилина'),
        (SECONDS, 'Секунда'),
    )

    code = models.CharField(max_length=50, verbose_name='Код задачі для контролю')
    host = models.ForeignKey(to=Server, verbose_name='Сервер', on_delete=models.PROTECT,
                             related_name="control_tasks")
    control_group = models.ForeignKey(to=TaskControlGroup, verbose_name='Група завдань', on_delete=models.PROTECT,
                                      related_name="control_tasks", blank=True, null=True, default=None)

    period = models.IntegerField(verbose_name='Період', default=1)
    period_multiply = models.IntegerField(verbose_name='Одиниці виміру', choices=INTERVALS, default=DAY)

    status = models.IntegerField(verbose_name='Код завершення', blank=True, null=True, default=None)
    message = models.CharField(max_length=250, default=None, blank=True, null=True)

    last_execute = models.DateTimeField(verbose_name="Час останнього виконання", blank=True, null=True, default=None)
    last_control = models.DateTimeField(verbose_name="Час контрольної перевірки", blank=True, null=True, default=None)
    last_message = models.DateTimeField(verbose_name="Час сповіщення", blank=True, null=True, default=None)

    notify_about_error = models.IntegerField(verbose_name='Сповіщати про помилки одразу', choices=NOTIFY,
                                             default=NOT_NOTYFY)

    def __str__(self):
        return f"{self.code} {self.host.name}"

    class Meta:
        unique_together = (("code", "host"),)
        verbose_name = 'Контроль автоматичних тасків'
        verbose_name_plural = 'Контроль автоматичних тасків'
        app_label = 'logview'
        db_table = 'task_logger_servertaskcontrol'
