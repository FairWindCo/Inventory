# Generated by Django 4.0.2 on 2023-02-14 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0007_servertaskadminproxy'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appinfoadminproxy',
            options={'verbose_name': "3. Зв'язок порталів та серверів", 'verbose_name_plural': "3. Зв'язок порталів та серверів"},
        ),
        migrations.AlterModelOptions(
            name='serverinfoadminproxy',
            options={'verbose_name': '1. ЗВІТ "СЕРВЕР"', 'verbose_name_plural': '1. ЗВІТ "СЕРВЕРИ"'},
        ),
        migrations.AlterModelOptions(
            name='specificationproxy',
            options={'verbose_name': 'Зони відповідальності серверів', 'verbose_name_plural': 'Зони відповідальності'},
        ),
    ]