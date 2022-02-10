# Generated by Django 4.0.2 on 2022-02-09 08:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Название приложения')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('url', models.CharField(blank=True, max_length=250, null=True, verbose_name='url')),
            ],
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform_name', models.CharField(default='virtual', max_length=200, verbose_name='Платформа')),
                ('num_cpu', models.PositiveIntegerField(default=1, verbose_name='CPU count')),
                ('cpu_type', models.CharField(default='virtual', max_length=200, verbose_name='Процессор')),
                ('ram', models.PositiveIntegerField(default=8, verbose_name='RAM, Gb')),
                ('description', models.TextField(verbose_name='Описание')),
                ('main_configuration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.configuration')),
            ],
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='имя домена')),
            ],
            options={
                'verbose_name': 'Справочник Доменов',
                'verbose_name_plural': 'Справочник Доменов',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='IP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(unique=True, verbose_name='IP адресс')),
            ],
        ),
        migrations.CreateModel(
            name='OS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='название ОС')),
            ],
            options={
                'verbose_name': 'Справочник ОС',
                'verbose_name_plural': 'Справочник ОС',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ResponsiblePerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='ФИО')),
                ('role', models.CharField(max_length=200, verbose_name='Квалификация')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
            ],
        ),
        migrations.CreateModel(
            name='ServerRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Роль сервера')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
            ],
        ),
        migrations.CreateModel(
            name='ServerRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='имя домена')),
            ],
            options={
                'verbose_name': 'Справочник Серверных',
                'verbose_name_plural': 'Справочник Серверных',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='SoftwareCatalog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Название приложения')),
            ],
            options={
                'verbose_name': 'Справочник Программ',
                'verbose_name_plural': 'Справочник Программ',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='имя сервера')),
                ('virtual_server_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='имя виртуальной машины')),
                ('os_version', models.CharField(blank=True, max_length=50, null=True, verbose_name='Версия ОС')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('has_internet_access', models.BooleanField(default=False, verbose_name='Имеет выход в интернет')),
                ('has_monitoring_agent', models.BooleanField(default=False, verbose_name='Мониторится агентом')),
                ('is_online', models.BooleanField(default=True, verbose_name='В эксплеатации')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Запись обновлена')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Запись создана')),
                ('os_last_update', models.DateTimeField(blank=True, null=True, verbose_name='Время последнего обнолвения')),
                ('last_update_id', models.CharField(blank=True, max_length=15, null=True, verbose_name='Последние апдейт')),
                ('os_installed', models.DateTimeField(blank=True, null=True, verbose_name='Система установлена')),
                ('version', models.PositiveIntegerField(default=0, editable=False, verbose_name='ver')),
                ('win_rm_access', models.BooleanField(default=True, verbose_name='WinRM доступ')),
                ('applications', models.ManyToManyField(blank=True, null=True, related_name='servers', to='info.Application')),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='info.domain', verbose_name='Домен')),
                ('ip_addresses', models.ManyToManyField(related_name='servers', to='info.IP')),
                ('os_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='info.os', verbose_name='ОС')),
                ('replaced_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='old_uses', to='info.server', verbose_name='заменен на')),
                ('roles', models.ManyToManyField(blank=True, null=True, related_name='servers', to='info.ServerRole')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='info.serverroom', verbose_name='сервреная')),
                ('updated_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='usernames', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('domain', 'name'),
            },
        ),
        migrations.CreateModel(
            name='HostInstalledSoftware',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=200, verbose_name='Версия')),
                ('installation_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата установки')),
                ('soft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.softwarecatalog', verbose_name='Программа')),
            ],
        ),
        migrations.CreateModel(
            name='DiskConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hdd_size', models.PositiveIntegerField(default=0, verbose_name='RAM, Gb')),
                ('hdd_type', models.PositiveIntegerField(choices=[(0, 'SATA HDD'), (1, 'SAS HDD'), (2, 'SATA SSD'), (3, 'M2 SSD')])),
                ('raid_type', models.PositiveIntegerField(choices=[(0, 'SATA HDD'), (1, 'SAS HDD'), (2, 'SATA SSD'), (3, 'M2 SSD')], default=999)),
                ('pool_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Платформа')),
                ('configuration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.configuration')),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='responsible',
            field=models.ManyToManyField(blank=True, null=True, to='info.ResponsiblePerson'),
        ),
        migrations.CreateModel(
            name='ServerAdminProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Состояние Серверов',
                'verbose_name_plural': 'Состояние Серверов',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('info.server',),
        ),
    ]
