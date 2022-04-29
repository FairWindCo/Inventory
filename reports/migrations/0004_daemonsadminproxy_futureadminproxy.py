# Generated by Django 4.0.2 on 2022-04-29 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0003_ip_mask_serverroom_net_masks_alter_serverroom_name_and_more'),
        ('reports', '0003_applicationserversspecificationproxy_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DaemonsAdminProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Служба',
                'verbose_name_plural': 'Службы',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('dictionary.serverservice',),
        ),
        migrations.CreateModel(
            name='FutureAdminProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Роли',
                'verbose_name_plural': 'Роли',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('dictionary.serverfuture',),
        ),
    ]
