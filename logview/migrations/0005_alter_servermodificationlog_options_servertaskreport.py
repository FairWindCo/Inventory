# Generated by Django 4.0.2 on 2023-02-14 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0012_alter_application_options_and_more'),
        ('logview', '0004_alter_servermodificationlog_log_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='servermodificationlog',
            options={'verbose_name': 'Журнал змін інформації', 'verbose_name_plural': 'Журнал змін інформації'},
        ),
        migrations.CreateModel(
            name='ServerTaskReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_date', models.DateTimeField(blank=True, null=True, verbose_name='Час')),
                ('info', models.CharField(max_length=250, verbose_name='Інформація')),
                ('is_error', models.BooleanField(default=False, verbose_name='Помилка')),
                ('server', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='reports', to='info.server', verbose_name='Сервер')),
            ],
            options={
                'verbose_name': 'Журнал автоматичних тасків',
                'verbose_name_plural': 'Журнал автоматичних тасків',
                'db_table': 'task_logger_servertaskreport',
            },
        ),
    ]
