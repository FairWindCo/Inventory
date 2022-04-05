# Generated by Django 4.0.2 on 2022-04-05 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServerService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Служба\\Демон')),
                ('display_name', models.CharField(max_length=200, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Служба\\Демон',
                'verbose_name_plural': 'Служба\\Демон',
                'ordering': ('name',),
            },
        ),
    ]
