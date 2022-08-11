# Generated by Django 4.0.2 on 2022-08-01 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0005_softwarecatalog_silent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='serverfuture',
            options={'ordering': ('name',), 'verbose_name': 'Роль (Future)', 'verbose_name_plural': 'Ролі (Futures)'},
        ),
        migrations.AlterModelOptions(
            name='serverservice',
            options={'ordering': ('name',), 'verbose_name': 'Служба (Демон)', 'verbose_name_plural': 'Служби (Демони)'},
        ),
        migrations.RemoveField(
            model_name='serverscheduledtask',
            name='display_name',
        ),
        migrations.AlterField(
            model_name='serverscheduledtask',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Запланована задача'),
        ),
        migrations.AlterField(
            model_name='serverservice',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Назва служби чи системного процессу'),
        ),
    ]