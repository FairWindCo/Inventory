from django.contrib.auth.models import User
from django.db import models

from dictionary.models import Domain, ServerRoom, OS, IP, SoftwareCatalog, ServerFuture
from .applications import HostInstalledSoftware


class Server(models.Model):
    name = models.CharField(max_length=50, verbose_name='имя сервера', unique=True)
    domain = models.ForeignKey(Domain, verbose_name='Домен', on_delete=models.PROTECT)
    os_name = models.ForeignKey(OS, verbose_name='ОС', on_delete=models.PROTECT, blank=True, null=True)
    room = models.ForeignKey(ServerRoom, verbose_name='сервреная', on_delete=models.PROTECT)
    virtual_server_name = models.CharField(max_length=50, verbose_name='имя виртуальной машины', blank=True, null=True)
    os_version = models.CharField(max_length=50, verbose_name='Версия ОС', blank=True, null=True)
    futures = models.ManyToManyField(ServerFuture, related_name='servers', blank=True)
    installed_soft = models.ManyToManyField(SoftwareCatalog, related_name='servers',
                                            through=HostInstalledSoftware, blank=True)
    ip_addresses = models.ManyToManyField(IP, related_name='servers')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    has_internet_access = models.BooleanField(verbose_name='Имеет выход в интернет', default=False)
    has_monitoring_agent = models.BooleanField(verbose_name='Мониторится агентом', default=False)
    is_online = models.BooleanField(verbose_name='В эксплеатации', default=True)
    replaced_by = models.ForeignKey("Server", verbose_name='заменен на', on_delete=models.PROTECT,
                                    related_name="old_uses", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Запись обновлена')
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Запись создана')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usernames', editable=False)
    os_last_update = models.DateTimeField(verbose_name='Время последнего обнолвения', blank=True, null=True)
    os_update_search = models.DateTimeField(verbose_name='Время авто поиска обнов.', blank=True, null=True)
    last_update_id = models.CharField(max_length=15, verbose_name='Последние апдейт', blank=True, null=True)
    os_installed = models.DateTimeField(verbose_name='Система установлена', blank=True, null=True)
    version = models.PositiveIntegerField(verbose_name='ver', default=0, editable=False)
    win_rm_access = models.BooleanField(verbose_name='WinRM доступ', default=True)

    @property
    def canonical_name(self):
        return f'{self.name}.{self.domain.name}' if self.domain else self.name

    @property
    def os_installed_humane(self):
        return self.os_installed.strftime("%d.%m.%Y %H:%M:%S") if self.os_installed else None

    @property
    def os_last_update_humane(self):
        return self.os_last_update.strftime("%d.%m.%Y %H:%M:%S") if self.os_last_update else None

    def ip_address_set(self):
        return ' '.join((ip['ip_address'] for ip in self.ip_addresses.values('ip_address')))

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.version += 1
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Сервер'
        verbose_name_plural = 'Серверы'
        ordering = ('domain', 'name')
