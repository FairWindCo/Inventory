from django.db import models


class ResponsiblePerson(models.Model):
    name = models.CharField(max_length=200, verbose_name='ФИО', unique=True)
    role = models.CharField(max_length=200, verbose_name='Квалификация')
    email = models.EmailField(verbose_name='email')


class Application(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название приложения', unique=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    url = models.CharField(max_length=250, verbose_name='url', blank=True, null=True)
    responsible = models.ManyToManyField(ResponsiblePerson)

    def __str__(self):
        return f'{self.name}'


class SoftwareCatalog(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название приложения', unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Справочник Программ'
        verbose_name_plural = 'Справочник Программ'


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


class ServerRole(models.Model):
    name = models.CharField(max_length=200, verbose_name='Роль сервера', unique=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    def __str__(self):
        return f'{self.name}'
