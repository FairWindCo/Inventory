from django.contrib.auth.models import User
from django.db import models

from dictionary.models import Domain, ServerRoom, OS, IP, SoftwareCatalog, ServerFuture, ServerService, \
    ServerScheduledTask
from .applications import HostInstalledSoftware, HostScheduledTask


class Server(models.Model):

    class ServerState(models.IntegerChoices):
        OFF = 0, 'Вимкнено'
        WORK = 1, 'В роботі'
        DELETED = 2, 'Видалено'
        RESERVED = 3, 'В резерві'
        INIT = 4, 'Не ініціалізовано'

    name = models.CharField(max_length=50, verbose_name='Ім`я сервера', unique=True)
    domain = models.ForeignKey(Domain, verbose_name='Домен', on_delete=models.PROTECT)
    os_name = models.ForeignKey(OS, verbose_name='ОС', on_delete=models.PROTECT, blank=True, null=True)
    room = models.ForeignKey(ServerRoom, verbose_name='Серверна', on_delete=models.PROTECT)
    virtual_server_name = models.CharField(max_length=50, verbose_name='Ім`я виртуальної машини', blank=True, null=True)
    os_version = models.CharField(max_length=50, verbose_name='Версія ОС', blank=True, null=True)
    futures = models.ManyToManyField(ServerFuture, related_name='servers', blank=True, verbose_name='Ролі (Futures)')
    daemons = models.ManyToManyField(ServerService, related_name='servers', blank=True, verbose_name='Сервіси (Services)')
    installed_soft = models.ManyToManyField(SoftwareCatalog, related_name='servers',
                                            through=HostInstalledSoftware, blank=True, verbose_name='Встановлене ПО')
    scheduled_tasks = models.ManyToManyField(ServerScheduledTask, related_name='task_servers',
                                             through=HostScheduledTask, blank=True, verbose_name='Запланованы задачі')
    ip_addresses = models.ManyToManyField(IP, related_name='servers')
    description = models.TextField(verbose_name='Примітки', blank=True, null=True)
    has_internet_access = models.BooleanField(verbose_name='Має вихід в інтернет', default=False)
    has_monitoring_agent = models.BooleanField(verbose_name='Відслідковується агентом', default=False)
    status = models.IntegerField(verbose_name='Стан', choices=ServerState.choices, default=ServerState.WORK)
    replaced_by = models.ForeignKey("Server", verbose_name='Змінено на', on_delete=models.PROTECT,
                                    related_name="old_uses", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Запис оновлена')
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Запис створено')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usernames', editable=False)
    os_last_update = models.DateTimeField(verbose_name='Час останнього оновлення', blank=True, null=True)
    os_update_search = models.DateTimeField(verbose_name='Час останнього пошуку оновлень', blank=True, null=True)
    last_update_id = models.CharField(max_length=15, verbose_name='Останній апдейт', blank=True, null=True)
    os_installed = models.DateTimeField(verbose_name='Система встановлена', blank=True, null=True)
    version = models.PositiveIntegerField(verbose_name='ver', default=0, editable=False)
    win_rm_access = models.BooleanField(verbose_name='WinRM доступ', default=True)
    external = models.BooleanField(verbose_name='Опублікований в Інтернет', default=False)

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
        self.name = self.name.upper()
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'{self.name}'

    help_text = 'Редагування інформації про сервери'
    form_help_text = 'Зміна інформації про один конкретний сервер'
    tooltip = 'Рдактор інформації про сервери'


    class Meta:
        verbose_name = '1. Сервер'
        verbose_name_plural = '1. Сервери'
        ordering = ('domain', 'name')
