from django.db import models


# Create your models here.
class Domain(models.Model):
    name = models.CharField(max_length=100, verbose_name='ім`я домену', unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('name',)
        verbose_name = 'Домен'
        verbose_name_plural = 'Домени'


class ServerRoom(models.Model):
    name = models.CharField(max_length=100, verbose_name='Назва серверної кімнати', unique=True)
    net_masks = models.ManyToManyField("IP", related_name='room',
                                       verbose_name='Мережеві маски, що використовуються у серверній',
                                       blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('name',)
        verbose_name = 'Серверна кімната'
        verbose_name_plural = 'Серверні кімнати'


class OS(models.Model):
    name = models.CharField(max_length=100, verbose_name='Назва ОС', unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('name',)
        verbose_name = 'ОС'
        verbose_name_plural = 'ОС'


class IP(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='IP адреса', unique=True)
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
    silent = models.BooleanField(verbose_name='Приховане значення', default=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Призначення серверу'
        verbose_name_plural = 'Призначення серверів'
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
    silent = models.BooleanField(verbose_name='Приховане значення', default=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Програма'
        verbose_name_plural = 'Програми'
        ordering = ('name',)


class ServerFuture(models.Model):
    name = models.CharField(max_length=100, verbose_name='Роль сервера', unique=True)
    display_name = models.CharField(max_length=200, verbose_name='Опис ролі', blank=True, null=True)
    silent = models.BooleanField(verbose_name='Приховане значення', default=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Роль (Future)'
        verbose_name_plural = 'Ролі (Futures)'
        ordering = ('name',)


class ServerService(models.Model):
    name = models.CharField(max_length=100, verbose_name='Назва служби чи системного процессу', unique=True)
    display_name = models.CharField(max_length=200, verbose_name='Опис', blank=True, null=True)
    silent = models.BooleanField(verbose_name='Приховане значення', default=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Служба (Демон)'
        verbose_name_plural = 'Служби (Демони)'
        ordering = ('name',)


class ServerScheduledTask(models.Model):
    name = models.CharField(max_length=200, verbose_name='Запланована задача')
    execute_path = models.CharField(max_length=255, verbose_name='Путь до скрипту')
    silent = models.BooleanField(verbose_name='Приховане значення', default=False)
    description = models.TextField(verbose_name='Опис', blank=True, null=True)


    def __str__(self):
        return f'{self.name} [{self.execute_path}]'

    class Meta:
        unique_together = ('name', 'execute_path')
        verbose_name = 'Автоматична задача'
        verbose_name_plural = 'Автоматичні задачі'
        ordering = ('name',)
