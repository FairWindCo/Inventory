from django.db import models

from dictionary.models import ServerResponse, SoftwareCatalog, ServerRole, ServerScheduledTask


class ResponsiblePerson(models.Model):
    name = models.CharField(max_length=200, verbose_name='ФІО', unique=True)
    role = models.CharField(max_length=200, verbose_name='Кваліфікації')
    email = models.EmailField(verbose_name='email')
    help_text = 'Перелік осіб, що відповідають за функціонування конкретного сервісу'
    form_help_text = 'Редагування даних відповідальної особи, для того, щоб родуміти з ким треба зв\'зуватися'
    tooltip = 'Редактор списка осіб відповідальних за роботу сервіса'

    class Meta:
        verbose_name = 'Особи відповідальні за сервіс'
        verbose_name_plural = 'Особи відповідальні за сервіс'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} {self.role} ({self.email})'


class Application(models.Model):
    name = models.CharField(max_length=200, verbose_name='Назва додатка', unique=True)
    description = models.TextField(verbose_name='Опис', blank=True, null=True)
    url = models.CharField(max_length=250, verbose_name='url', blank=True, null=True)
    monitoring_url = models.CharField(max_length=250, verbose_name='Моніторінг url', blank=True, null=True)
    worked_servers = models.ManyToManyField("Server", related_name='applications', blank=True,
                                            through="ApplicationServers")
    responsible = models.ManyToManyField(ResponsiblePerson, blank=True)
    depends = models.ManyToManyField(to="Application", related_name='dependencies', blank=True,
                                     verbose_name='Залежить від')
    external = models.BooleanField(verbose_name='Опублікована в Інтернет', default=False)

    help_text = 'Редактор переліку сервісів, які є доступними для клієнтів'
    form_help_text = 'Редагування інформації про сервіси, що надаються клієнтам'
    tooltip = 'Редагування описів сервісів, які надаються клієнтам'


    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = '2. Сервіс'
        verbose_name_plural = '2. Сервіс'
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

    help_text = 'Редагування зв\'язку між сервісами та серверами, що задіяни для забезпечення їх роботи'
    form_help_text = 'Редагування зв\'язку між сервісами та серверами, що задіяни для забезпечення їх роботи'
    tooltip = 'Редагування зв\'язку між сервісами та серверами, що задіяни для забезпечення їх роботи'


    def __str__(self):
        return f'{self.server.name} - {self.application.name}'

    class Meta:
        verbose_name = '3. Зв\'язок Сервер - Сервіс'
        verbose_name_plural = '3. Зв\'язок Сервер - Сервіс'
        ordering = ('server__name', 'application__name')


class HostInstalledSoftware(models.Model):
    soft = models.ForeignKey(SoftwareCatalog, on_delete=models.CASCADE, verbose_name='Додаток',
                             related_name='installs')
    server = models.ForeignKey("Server", on_delete=models.CASCADE, verbose_name='Сервер', related_name='host_soft')
    version = models.CharField(max_length=200, verbose_name='Версія')
    installation_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата встановлення')
    last_check_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата перевірики')
    is_removed = models.BooleanField(default=False, verbose_name='ПО видалено')

    help_text = 'Редагування переліку програм, що встановлені на сервери'
    form_help_text = 'Редагування однієї конкретної позиції, що на якому сервері встановлено'
    tooltip = 'Редактор ПО встановлено на сервері'


    def __str__(self):
        return f'{self.server.name} {self.soft.name} {self.version}'


    class Meta:
        unique_together = (('soft', 'server'),)
        verbose_name = 'ПО встановлено на сервері'
        verbose_name_plural = 'ПО встановлено на сервері'


class HostScheduledTask(models.Model):
    task = models.ForeignKey(ServerScheduledTask, on_delete=models.CASCADE, verbose_name='Додаток',
                             related_name='tasks')
    server = models.ForeignKey("Server", on_delete=models.CASCADE, verbose_name='Сервер', related_name='host_task')
    run_user = models.CharField(max_length=50, verbose_name='Користувач', blank=True, null=True)
    author = models.CharField(max_length=50, verbose_name='Автор', blank=True, null=True)
    schedule_type = models.CharField(max_length=150, verbose_name='Тип Повторення', blank=True, null=True)
    schedule = models.CharField(max_length=150, verbose_name='Повторення', blank=True, null=True)
    installation_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата встановлення')
    last_run = models.DateTimeField(blank=True, null=True, verbose_name='Дата останього запуску')
    next_run = models.DateTimeField(blank=True, null=True, verbose_name='Дата наступного запуску')
    status = models.CharField(max_length=50, verbose_name='Статус', blank=True, null=True)
    exit_code = models.CharField(max_length=50, verbose_name='Останній код виконання', blank=True, null=True)
    last_check_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата перевірики')
    is_removed = models.BooleanField(default=False, verbose_name='Задачу видалено')

    help_text = 'Редагування переліку автоматичних завдань, що працюють на серверах'
    form_help_text = 'Редагування інформації про один конкретний таск на конкретному сервері'
    tooltip = 'Редактор переліку автоматичних завдань на серверах'


    def __str__(self):
        return f'{self.server.name} {self.task.name} {self.installation_date}'

    class Meta:
        unique_together = (('task', 'server'),)
        verbose_name = 'Заплановані задачі'
        verbose_name_plural = 'Запланована задача'
        ordering = ('server__name', 'task__name')
