from django.db import models


# Create your models here.
from info.models import Server


class ServerTaskReport(models.Model):
    server = models.ForeignKey(Server, verbose_name='Сервер', on_delete=models.PROTECT,
                               related_name="reports", blank=True, null=True)
    report_date = models.DateTimeField(verbose_name='Время', blank=True, null=True)
    info = models.CharField(max_length=250, verbose_name='Информация')
    is_error = models.BooleanField(verbose_name='Ошибка', default=False)
