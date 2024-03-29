# Generated by Django 4.2.1 on 2024-03-27 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faci', '0015_remove_facicanvas_other_agreements_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='facicanvas',
            name='when_finished',
            field=models.DateTimeField(null=True, verbose_name='Дата фактического окончания встречи'),
        ),
        migrations.AddField(
            model_name='facicanvas',
            name='when_started',
            field=models.DateTimeField(null=True, verbose_name='Дата фактического начала встречи'),
        ),
    ]
