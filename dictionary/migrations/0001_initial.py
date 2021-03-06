# Generated by Django 4.0.2 on 2022-02-15 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='имя домена')),
            ],
            options={
                'verbose_name': 'Домен',
                'verbose_name_plural': 'Домены',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='IP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(unique=True, verbose_name='IP адресс')),
            ],
            options={
                'verbose_name': 'IP',
                'verbose_name_plural': 'IP',
            },
        ),
        migrations.CreateModel(
            name='OS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='название ОС')),
            ],
            options={
                'verbose_name': 'ОС',
                'verbose_name_plural': 'ОС',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ServerFuture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Роль/Оснастка сервера')),
                ('display_name', models.CharField(max_length=200, verbose_name='Описание роли')),
            ],
            options={
                'verbose_name': 'Роль/Оснастка',
                'verbose_name_plural': 'Роли/Оснастки',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ServerResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Отвественность')),
            ],
            options={
                'verbose_name': 'Отвественность',
                'verbose_name_plural': 'Отвественности',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ServerRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Роль сервера')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Роль Приложения',
                'verbose_name_plural': 'Роли Приложения',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ServerRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='имя домена')),
            ],
            options={
                'verbose_name': 'Серверная',
                'verbose_name_plural': 'Серверных',
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
                'verbose_name': 'Программа',
                'verbose_name_plural': 'Программы',
                'ordering': ('name',),
            },
        ),
    ]
