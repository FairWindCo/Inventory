from django.db import models

from dictionary.models import ServerResponse, SoftwareCatalog, ServerRole


class ResponsiblePerson(models.Model):
    name = models.CharField(max_length=200, verbose_name='ФІО', unique=True)
    role = models.CharField(max_length=200, verbose_name='Кваліфікації')
    email = models.EmailField(verbose_name='email')

    class Meta:
        verbose_name = 'Відповідальні особи'
        verbose_name_plural = 'Відповідальні особи'
        ordering = ('name',)


class Application(models.Model):
    name = models.CharField(max_length=200, verbose_name='Назва додатка', unique=True)
    description = models.TextField(verbose_name='Опис', blank=True, null=True)
    url = models.CharField(max_length=250, verbose_name='url', blank=True, null=True)
    monitoring_url = models.CharField(max_length=250, verbose_name='Моніторінг url', blank=True, null=True)
    worked_servers = models.ManyToManyField("Server", related_name='applications', blank=True,
                                            through="ApplicationServers")
    responsible = models.ManyToManyField(ResponsiblePerson, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Додаток'
        verbose_name_plural = 'Додаток'
        ordering = ('name',)


class ApplicationServersSpecification(models.Model):
    application_server = models.ForeignKey("ApplicationServers", on_delete=models.CASCADE, verbose_name='Призначенн',
                                           related_name='specification')
    role = models.ForeignKey(ServerRole, on_delete=models.CASCADE, verbose_name='Роль', blank=True, null=True)
    response = models.ForeignKey(ServerResponse, on_delete=models.CASCADE, verbose_name='Відповідальність', blank=True,
                                 null=True)
    description = models.TextField(verbose_name='Опис', blank=True, null=True)
    response_person = models.ForeignKey(ResponsiblePerson, on_delete=models.CASCADE,
                                        verbose_name='Відповідальний співробітник', blank=True,
                                        null=True)

    def __str__(self):
        return f'{self.application_server.application}'

    class Meta:
        verbose_name = 'Зона відповідальності'
        verbose_name_plural = 'Зони відповідальності'


class ApplicationServers(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, verbose_name='Додаток',
                                    related_name='app_server')
    server = models.ForeignKey("Server", on_delete=models.CASCADE, verbose_name='Сервер', related_name='app_info')
    specifications = models.ManyToManyField(ServerRole, verbose_name='Призначення', blank=True,
                                            through=ApplicationServersSpecification)
    description = models.TextField(verbose_name='Опис', blank=True, null=True)

    def __str__(self):
        return f'{self.server.name} - {self.application.name}'

    class Meta:
        verbose_name = 'Сервер для додатка'
        verbose_name_plural = 'Сервера для додатка'
        ordering = ('server__name', 'application__name')


class HostInstalledSoftware(models.Model):
    soft = models.ForeignKey(SoftwareCatalog, on_delete=models.CASCADE, verbose_name='Додаток',
                             related_name='installs')
    server = models.ForeignKey("Server", on_delete=models.CASCADE, verbose_name='Сервер', related_name='host_soft')
    version = models.CharField(max_length=200, verbose_name='Версія')
    installation_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата встановлення')
    last_check_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата перевірики')
    is_removed = models.BooleanField(default=False, verbose_name='ПО видалено')

    def __str__(self):
        return f'{self.server.name} {self.soft.name} {self.version} {self.installation_date}'

    class Meta:
        unique_together = (('soft', 'server'),)
        verbose_name = 'Встановлене ПО'
        verbose_name_plural = 'Встановлене ПО'
        ordering = ('server__name', 'soft__name')
