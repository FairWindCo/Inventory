from django.db import models

from info.models import Server


class Configuration(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE, verbose_name='Сервер', related_name='hardware')
    platform_name = models.CharField(max_length=200, verbose_name='Платформа', default='virtual')
    num_cpu = models.PositiveIntegerField(verbose_name='CPU count', default=1)
    num_cores = models.PositiveIntegerField(verbose_name='CPU Core count', default=1)
    num_virtual = models.PositiveIntegerField(verbose_name='HT count', default=1)
    cpu_type = models.CharField(max_length=200, verbose_name='Процессор', default='virtual')
    ram = models.PositiveIntegerField(verbose_name='RAM, Gb', default=8)
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.platform_name}'

    class Meta:
        verbose_name = 'Конфигурация'
        verbose_name_plural = 'Конфигурации'
        ordering = ('server__name', 'platform_name')


class HDDType(models.IntegerChoices):
    SATA = 0, 'SATA HDD'
    SAS = 1, 'SAS HDD'
    SSD = 2, 'SATA SSD'
    M2 = 3, 'M2 SSD'
    VIRTUAL = 50, 'Virtual'


class RAIDType(models.IntegerChoices):
    NO_RAID = 999, '---'
    ZERO = 0, 'RAID 0'
    ONE = 1, 'RAID 1'
    ZERO_ONE = 2, 'RAID 1+0'
    FIVE = 3, 'RAID 5'
    TEN = 4, 'RAID 10'


class DiskConfiguration(models.Model):
    configuration = models.ForeignKey(Configuration, on_delete=models.CASCADE, related_name='disks')
    pool_name = models.CharField(max_length=200, verbose_name='Платформа', blank=True, null=True)
    hdd_size = models.PositiveIntegerField(verbose_name='HDD, Gb', default=0)
    hdd_type = models.PositiveIntegerField(choices=HDDType.choices, blank=True, null=True, verbose_name='Тип диска')
    raid_type = models.PositiveIntegerField(choices=HDDType.choices, default=RAIDType.NO_RAID, verbose_name='Тип RAID')

    def __str__(self):
        return f'{self.pool_name} {self.hdd_size}GB'

    class Meta:
        verbose_name = 'Диск'
        verbose_name_plural = 'Диски'
        ordering = ('configuration__server__name', 'pool_name')
