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


class InstalledSoftware(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название приложения', unique=True)

    def __str__(self):
        return f'{self.name}'


class ServerRole(models.Model):
    name = models.CharField(max_length=200, verbose_name='Роль сервера', unique=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    def __str__(self):
        return f'{self.name}'
