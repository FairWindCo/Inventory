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
    name = models.CharField(max_length=100, verbose_name='имя серверной', unique=True)
    net_masks = models.ManyToManyField("IP", related_name='room',
                                       verbose_name='сетевые маски',
                                       blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('name',)
        verbose_name = 'Серверна кімната'
        verbose_name_plural = 'Серверні кімнати'


class OS(models.Model):
    name = models.CharField(max_length=100, verbose_name='назва ОС', unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('name',)
        verbose_name = 'ОС'
        verbose_name_plural = 'ОС'


class IP(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='IP адрес', unique=True)
    mask = models.PositiveIntegerField(verbose_name='Маска', default=32)

    def __str__(self):
        if self.mask < 32:
            return f'{self.ip_address}/{self.mask}'
        return f'{self.ip_address}'

    class Meta:
        verbose_name = 'IP'
        verbose_name_plural = 'IP'
        unique_together = ('ip_address', 'mask')


class ServerRole(models.Model):
    name = models.CharField(max_length=200, verbose_name='Призначення сервера', unique=True)
    description = models.TextField(verbose_name='Опис', blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Призначення додатку'
        verbose_name_plural = 'Призначення додатків'
        ordering = ('name',)


class ServerResponse(models.Model):
    name = models.CharField(max_length=200, verbose_name='Відповідальність', unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Відповідальність'
        verbose_name_plural = 'Відповідальності'
        ordering = ('name',)


class SoftwareCatalog(models.Model):
    name = models.CharField(max_length=200, verbose_name='Назва програми', unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Програма'
        verbose_name_plural = 'Програми'
        ordering = ('name',)


class ServerFuture(models.Model):
    name = models.CharField(max_length=100, verbose_name='Роль сервера', unique=True)
    display_name = models.CharField(max_length=200, verbose_name='Опис ролі')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Ролі'
        ordering = ('name',)


class ServerService(models.Model):
    name = models.CharField(max_length=100, verbose_name='Сервіс', unique=True)
    display_name = models.CharField(max_length=200, verbose_name='Опис')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Сервіс'
        verbose_name_plural = 'Сервіси'
        ordering = ('name',)
