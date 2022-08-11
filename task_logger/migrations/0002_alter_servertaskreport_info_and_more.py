# Generated by Django 4.0.2 on 2022-08-01 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_logger', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servertaskreport',
            name='info',
            field=models.CharField(max_length=250, verbose_name='Інформація'),
        ),
        migrations.AlterField(
            model_name='servertaskreport',
            name='is_error',
            field=models.BooleanField(default=False, verbose_name='Помилка'),
        ),
        migrations.AlterField(
            model_name='servertaskreport',
            name='report_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Час'),
        ),
    ]