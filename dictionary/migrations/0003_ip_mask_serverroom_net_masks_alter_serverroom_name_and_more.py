# Generated by Django 4.0.2 on 2022-04-29 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0002_serverservice'),
    ]

    operations = [
        migrations.AddField(
            model_name='ip',
            name='mask',
            field=models.PositiveIntegerField(default=32, max_length=2, verbose_name='Маска'),
        ),
        migrations.AddField(
            model_name='serverroom',
            name='net_masks',
            field=models.ManyToManyField(blank=True, null=True, related_name='room', to='dictionary.IP', verbose_name='сетевые маски'),
        ),
        migrations.AlterField(
            model_name='serverroom',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='имя серверной'),
        ),
        migrations.AlterUniqueTogether(
            name='ip',
            unique_together={('ip_address', 'mask')},
        ),
    ]
