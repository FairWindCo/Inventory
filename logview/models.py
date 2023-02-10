from django.db import models

# Create your models here.
from info.models import Server


class ServerModificationLog(models.Model):
    class LogType(models.IntegerChoices):
        DEBUG = 0, 'DEBUG'
        INFO = 1, 'Інформація'
        WARNING = 2, 'Попередження'
        ERROR = 3, 'Помилка'
        CRITICAL = 4, 'Тривога'
        INSTALL = 10, 'Встановлення'
        UPDATE = 11, 'Оновлення'
        REMOVED = 12, 'Видалення'

    class LogTopic(models.IntegerChoices):
        OTHER = 0, 'Інше'
        TASK = 1, 'Задачі'
        SERVICE = 2, 'Служби'
        SOFT = 3, 'ПО'
        ROLE = 4, 'Призначення'
        FUTURE = 5, 'Роль'
        APP = 6, 'Сервіс'
        SYSTEM = 7, 'Система'

    server = models.ForeignKey(Server, on_delete=models.CASCADE, verbose_name='Сервер')
    seen = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    description = models.CharField(max_length=255, verbose_name='Опис')
    log_type = models.IntegerField(choices=LogType.choices, default=LogType.INFO, verbose_name='Тип')
    topic = models.IntegerField(choices=LogTopic.choices, default=LogTopic.OTHER, verbose_name='Розділ')

    help_text = 'Журнал в якій заноситься інформація про зафіксовані зміни в конфігурації серверів'
    form_help_text = 'Зміни що зафіксовани в інформації про конкретний сервер'
    tooltip = 'Журнал змін, що відбувалися в конфігурації серверу'


    class Meta:
        verbose_name = 'Журнал змін інформації'
        verbose_name_plural = 'Журнал змін інформації'

    def __str__(self):
        return f'{self.seen.strftime("%d.%m.%y %H:%M:%S")} {self.server.name}'
