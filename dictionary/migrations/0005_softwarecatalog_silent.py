# Generated by Django 4.0.2 on 2022-08-01 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0004_serverscheduledtask_alter_domain_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='softwarecatalog',
            name='silent',
            field=models.BooleanField(default=False, verbose_name='Приховане значення'),
        ),
    ]
