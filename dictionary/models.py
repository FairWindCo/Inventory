from django.db import models


# Create your models here.
class Domain(models.Model):
    name = models.CharField(max_length=100, verbose_name='имя домена', unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('name',)
        verbose_name = 'Домен'
        verbose_name_plural = 'Домены'


class ServerRoom(models.Model):
    name = models.CharField(max_length=100, verbose_name='имя домена', unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('name',)
        verbose_name = 'Серверная'
        verbose_name_plural = 'Серверных'


class OS(models.Model):
    name = models.CharField(max_length=100, verbose_name='название ОС', unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('name',)
        verbose_name = 'ОС'
        verbose_name_plural = 'ОС'


class IP(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='IP адресс', unique=True)

    def __str__(self):
        return f'{self.ip_address}'

    class Meta:
        verbose_name = 'IP'
        verbose_name_plural = 'IP'


class ServerRole(models.Model):
    name = models.CharField(max_length=200, verbose_name='Роль сервера', unique=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Роль Приложения'
        verbose_name_plural = 'Роли Приложения'
        ordering = ('name',)


class ServerResponse(models.Model):
    name = models.CharField(max_length=200, verbose_name='Отвественность', unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Отвественность'
        verbose_name_plural = 'Отвественности'
        ordering = ('name',)


class SoftwareCatalog(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название приложения', unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Программа'
        verbose_name_plural = 'Программы'
        ordering = ('name',)


class ServerFuture(models.Model):
    name = models.CharField(max_length=100, verbose_name='Роль/Оснастка сервера', unique=True)
    display_name = models.CharField(max_length=200, verbose_name='Описание роли')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Роль/Оснастка'
        verbose_name_plural = 'Роли/Оснастки'
        ordering = ('name',)


class ServerService(models.Model):
    name = models.CharField(max_length=100, verbose_name='Служба\Демон', unique=True)
    display_name = models.CharField(max_length=200, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Служба\Демон'
        verbose_name_plural = 'Служба\Демон'
        ordering = ('name',)
