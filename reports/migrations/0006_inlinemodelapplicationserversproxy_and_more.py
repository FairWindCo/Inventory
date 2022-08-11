# Generated by Django 4.0.2 on 2022-08-01 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0009_hostscheduledtask_alter_application_options_and_more'),
        ('reports', '0005_alter_appinfoadminproxy_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='InlineModelApplicationServersProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Задіяний сервер',
                'verbose_name_plural': 'Задіяні сервери',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('info.applicationservers',),
        ),
        migrations.AlterModelOptions(
            name='appinfoadminproxy',
            options={'verbose_name': 'СЕРВІС ТА СЕРВЕРИ', 'verbose_name_plural': '!СЕРВІСИ ТА СЕРВЕРИ'},
        ),
        migrations.AlterModelOptions(
            name='appinfoaproxy',
            options={'verbose_name': 'СЕРВІС', 'verbose_name_plural': '!СЕРВІСИ'},
        ),
        migrations.AlterModelOptions(
            name='serverinfoadminproxy',
            options={'verbose_name': 'СЕРВЕР', 'verbose_name_plural': '!СЕРВЕРИ'},
        ),
    ]