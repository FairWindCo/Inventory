from django.db import models

# Create your models here.
from info.models import Server


class ServerModificationLog(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE, verbose_name='Сервер')
    seen = models.DateTimeField(auto_now_add=True, verbose_name='Дата события')
    description = models.CharField(max_length=255, verbose_name='Описание')

    class Meta:
        verbose_name = 'Журнал'
        verbose_name_plural = 'Журнал'

    def __str__(self):
        return f'{self.seen.strftime("%d.%m.%y %H:%M:%S")} {self.server.name}'
