from django.db import models


class Configuration(models.Model):
    platform_name = models.CharField(max_length=200, verbose_name='Платформа', default='virtual')
    num_cpu = models.PositiveIntegerField(verbose_name='CPU count', default=1)
    cpu_type = models.CharField(max_length=200, verbose_name='Процессор', default='virtual')
    ram = models.PositiveIntegerField(verbose_name='RAM, Gb', default=8)
    description = models.TextField(verbose_name='Описание')
    main_configuration = models.ForeignKey("Configuration", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.platform_name}'


class HDDType(models.IntegerChoices):
    SATA = 0, 'SATA HDD'
    SAS = 1, 'SAS HDD'
    SSD = 2, 'SATA SSD'
    M2 = 3, 'M2 SSD'


class RAIDType(models.IntegerChoices):
    NO_RAID = 999, '---'
    ZERO = 0, 'RAID 0'
    ONE = 1, 'RAID 1'
    ZERO_ONE = 2, 'RAID 1+0'
    FIVE = 3, 'RAID 5'
    TEN = 4, 'RAID 10'


class DiskConfiguration(models.Model):
    configuration = models.ForeignKey(Configuration, on_delete=models.CASCADE)
    hdd_size = models.PositiveIntegerField(verbose_name='RAM, Gb', default=0)
    hdd_type = models.PositiveIntegerField(choices=HDDType.choices)
    raid_type = models.PositiveIntegerField(choices=HDDType.choices, default=RAIDType.NO_RAID)
    pool_name = models.CharField(max_length=200, verbose_name='Платформа', blank=True, null=True)
