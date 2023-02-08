# Generated by Django 3.2.10 on 2023-02-08 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faci', '0014_auto_20230204_0532'),
    ]

    operations = [
        migrations.AddField(
            model_name='facicanvas',
            name='meeting_status',
            field=models.IntegerField(choices=[(1, 'Редактируется'), (2, 'Началась'), (3, 'Окончена')], default=1, verbose_name='Статус встречи'),
        ),
    ]
