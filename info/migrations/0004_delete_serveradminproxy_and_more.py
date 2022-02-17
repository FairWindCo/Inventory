# Generated by Django 4.0.2 on 2022-02-16 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0003_alter_applicationservers_response_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ServerAdminProxy',
        ),
        migrations.RemoveField(
            model_name='configuration',
            name='main_configuration',
        ),
        migrations.AddField(
            model_name='configuration',
            name='num_cores',
            field=models.PositiveIntegerField(default=1, verbose_name='CPU Core count'),
        ),
        migrations.AddField(
            model_name='configuration',
            name='num_virtual',
            field=models.PositiveIntegerField(default=1, verbose_name='HT count'),
        ),
        migrations.AddField(
            model_name='configuration',
            name='server',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='hardware', to='info.server', verbose_name='Сервер'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='diskconfiguration',
            name='hdd_type',
            field=models.PositiveIntegerField(blank=True, choices=[(0, 'SATA HDD'), (1, 'SAS HDD'), (2, 'SATA SSD'), (3, 'M2 SSD'), (50, 'Virtual')], null=True),
        ),
        migrations.AlterField(
            model_name='diskconfiguration',
            name='raid_type',
            field=models.PositiveIntegerField(choices=[(0, 'SATA HDD'), (1, 'SAS HDD'), (2, 'SATA SSD'), (3, 'M2 SSD'), (50, 'Virtual')], default=999),
        ),
    ]
