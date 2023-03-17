from ipaddress import ip_address, ip_network

from django.db import models


# Create your models here.
class Domain(models.Model):
    name = models.CharField(max_length=100, verbose_name='ім`я домену', unique=True)
    help_text = 'Цей довідник використовується для заповнення інформацію про домен до якого включено сервер ' \
                '(довідник потріден, так як одне й те саме значення може бути на більше ніж одному сервері)'
    form_help_text = 'Назва домену, що буде використана при заповнені інформації про сервер'
    tooltip = 'Довідник доменів, що використовується в системі'

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
    help_text = 'Цей довідник використовується для заповнення інформацію серверну в якій розміщено сервер ' \
                '(довідник потріден, так як одне й те саме значення може бути на більше ніж одному сервері)'
    form_help_text = 'Назва серверної, що буде використана при заповнені інформації про сервер'
    tooltip = 'Довідник серверних, що використовується в системі'

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('name',)
        verbose_name = 'Серверна кімната'
        verbose_name_plural = 'Серверні кімнати'


class OS(models.Model):
    name = models.CharField(max_length=100, verbose_name='Назва ОС', unique=True)
    help_text = 'Цей довідник використовується для заповнення інформацію про сімейство ОС сервера ' \
                '(довідник потріден, так як одне й те саме значення може бути на більше ніж одному сервері)'
    form_help_text = 'Назва операційної системи, що буде використана при заповнені інформації про сервер'
    tooltip = 'Довідник ОС, що використовується в системі'

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('name',)
        verbose_name = 'ОС'
        verbose_name_plural = 'ОС'


class IP(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='IP адреса', unique=True)
    mask = models.PositiveIntegerField(verbose_name='Маска', default=32)
    comment = models.CharField(verbose_name='Коментар', max_length=250, default='', blank=True, null=True)
    help_text = 'Цей довідник ІР адрес використовується для заповнення інформацію про домен до якого включено сервер ' \
                '(довідник потріден, так як одне й те саме значення може бути на більше ніж одному сервері)'
    form_help_text = 'Заповнюється інформація про конкретну ІР адресу, що використовується сервером'
    tooltip = 'Довідник ІР, що використовується в системі'

    def get_server_names(self):
        return ','.join([server.name for server in self.servers.all()]) if self.servers else ''

    def __str__(self):
        if self.mask < 32:
            return f'{self.ip_address}/{self.mask}{"(" + self.comment + ")" if self.comment else ""}'
        return f'{self.ip_address}{"(" + self.comment + ")" if self.comment else ""}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.mask < 0:
            self.mask = 0
        if self.mask < 32:
            self.ip_address = str(ip_network(f'{self.ip_address}/{self.mask}', False).network_address)
        super().save(force_insert, force_update, using, update_fields)

    def get_network_address(self):
        if self.mask == 32:
            return []
        #print(self.mask)
        host_part = 32 - self.mask
        mask = (1 << 32) - (1 << host_part)
        my_net = int(ip_address(self.ip_address)) & mask

        return [ip for ip in IP.objects.all() if ip.mask == 32 and (int(ip_address(ip.ip_address)) & mask) == my_net]

    class Meta:
        verbose_name = 'IP'
        verbose_name_plural = 'IP'
        unique_together = ('ip_address', 'mask')


class ServerRole(models.Model):
    name = models.CharField(max_length=200, verbose_name='Призначення сервера', unique=True)
    description = models.TextField(verbose_name='Опис', blank=True, null=True)
    silent = models.BooleanField(verbose_name='Приховане значення', default=False)
    help_text = 'Цей довідник задає перелік доступних в системі "ролей", що виконує сервер. ' \
                'Використовується при заповненні інформації про існуючи портали ' \
                '(довідник потріден, так як одне й те саме значення може бути на більше ніж одному сервері)'
    form_help_text = 'Назва призначення серверу, що буде використана при заповнені ' \
                     'ролі сервера в роботі конкретного порталу чи служби'
    tooltip = 'Довідник ролей, що використовується в системі'

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Призначення серверу'
        verbose_name_plural = 'Призначення серверів'
        ordering = ('name',)


class ServerResponse(models.Model):
    name = models.CharField(max_length=200, verbose_name='Відповідальність', unique=True)
    help_text = 'Цей довідник задає перелік значень відповідальності, що вказуються в описах порталів, яку' \
                'відповідальність несе конкретний сервер в роботі вказаного порталу ' \
                '(довідник потріден, так як одне й те саме значення може бути на більше ніж одному сервері)'
    form_help_text = 'Відповідальність, що вказуються в описах порталів, якє' \
                     ' значення має робота сервера для вказаного порталу'
    tooltip = 'Довідник "Відповідальностей серверів", що використовується в системі'

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Відповіmiдальність'
        verbose_name_plural = 'Відповідальності'
        ordering = ('name',)


class SoftwareCatalog(models.Model):
    name = models.CharField(max_length=200, verbose_name='Назва програми', unique=True)
    silent = models.BooleanField(verbose_name='Приховане значення', default=False)
    help_text = 'Цей довідник назв програм, що встановлені на сервери ' \
                '(довідник потріден, так як одне й те саме значення може бути на більше ніж одному сервері)'
    form_help_text = 'Назва программи, що встановлена на сервер без версії'
    tooltip = 'Довідник назв программ, що використовується в системі'

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Програма (Soft Name)'
        verbose_name_plural = 'Програми (Softs Name)'
        ordering = ('name',)


class ServerFuture(models.Model):
    name = models.CharField(max_length=100, verbose_name='Роль сервера', unique=True)
    display_name = models.CharField(max_length=200, verbose_name='Опис ролі', blank=True, null=True)
    silent = models.BooleanField(verbose_name='Приховане значення', default=False)
    help_text = 'Цей довідник назв Windows Future, що встановлені на сервери ' \
                '(довідник потріден, так як одне й те саме значення може бути на більше ніж одному сервері)'
    form_help_text = 'Назва Windows Future, що встановлена на сервер без версії'
    tooltip = 'Довідник назв компонентів системи, що використовується'

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
    help_text = 'Цей довідник назв служб та демонів, що працюють на сервері ' \
                '(довідник потріден, так як одне й те саме значення може бути на більше ніж одному сервері)'
    form_help_text = 'Назва служби\демона, що працює на сервері'
    tooltip = 'Довідник назв служб, що використовується в системі'

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Служба (Service)'
        verbose_name_plural = 'Служби (Service)'
        ordering = ('name',)


class ServerScheduledTask(models.Model):
    name = models.CharField(max_length=200, verbose_name='Запланована задача')
    execute_path = models.CharField(max_length=255, verbose_name='Путь до скрипту')
    silent = models.BooleanField(verbose_name='Приховане значення', default=False)
    description = models.TextField(verbose_name='Опис', blank=True, null=True)
    code = models.CharField(max_length=50, verbose_name='Код задачі для контролю', blank=True, null=True, default=None)

    help_text = 'Цей довідник завдань (tasks), що працюють на сервері ' \
                ' (довідник потріден, так як одне й те саме значення може бути на більше ніж одному сервері)'
    form_help_text = 'Опис такси, що працює на сервері'
    tooltip = 'Довідник автоматичних задач, що використовується в системі'

    def __str__(self):
        return f'{self.name} [{self.execute_path}]'

    class Meta:
        unique_together = ('name', 'execute_path')
        verbose_name = 'Автоматична задача'
        verbose_name_plural = 'Автоматичні задачі'
        ordering = ('name',)
