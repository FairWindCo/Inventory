from django.db import models

from dictionary.models import ServerResponse, SoftwareCatalog, ServerRole


class ResponsiblePerson(models.Model):
    name = models.CharField(max_length=200, verbose_name='ФИО', unique=True)
    role = models.CharField(max_length=200, verbose_name='Квалификация')
    email = models.EmailField(verbose_name='email')

    class Meta:
        verbose_name = 'Справочник Отвественных'
        verbose_name_plural = 'Справочник Отвественных'
        ordering = ('name',)


class Application(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название приложения', unique=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    url = models.CharField(max_length=250, verbose_name='url', blank=True, null=True)
    monitoring_url = models.CharField(max_length=250, verbose_name='url', blank=True, null=True)
    worked_servers = models.ManyToManyField("Server", related_name='servers', blank=True, through="ApplicationServers")
    responsible = models.ManyToManyField(ResponsiblePerson)

    def __str__(self):
        return f'{self.name}'


class ApplicationServers(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, verbose_name='Программа')
    server = models.ForeignKey("Server", on_delete=models.CASCADE, verbose_name='Сервер')
    role = models.ForeignKey(ServerRole, on_delete=models.CASCADE, verbose_name='Роль', blank=True, null=True)
    response = models.ForeignKey(ServerResponse, on_delete=models.CASCADE, verbose_name='Ответственнность', blank=True,
                                 null=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)


class HostInstalledSoftware(models.Model):
    soft = models.ForeignKey(SoftwareCatalog, on_delete=models.CASCADE, verbose_name='Программа')
    server = models.ForeignKey("Server", on_delete=models.CASCADE, verbose_name='Сервер')
    version = models.CharField(max_length=200, verbose_name='Версия')
    installation_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата установки')
    last_check_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата проверки')
    is_removed = models.BooleanField(default=False, verbose_name='Софт удален')

    def __str__(self):
        return f'{self.server.name} {self.soft.name} {self.version} {self.installation_date}'

    class Meta:
        unique_together = (('soft', 'server'),)
        verbose_name = 'Установленный софт'
        verbose_name_plural = 'Установленный софт'
        ordering = ('server__name', 'soft__name')
