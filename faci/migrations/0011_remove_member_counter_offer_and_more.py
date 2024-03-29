# Generated by Django 4.2.1 on 2024-03-24 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faci', '0010_expression'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='counter_offer',
        ),
        migrations.RemoveField(
            model_name='member',
            name='fundamental_objections',
        ),
        migrations.RemoveField(
            model_name='member',
            name='questions',
        ),
        migrations.RemoveField(
            model_name='member',
            name='suggested_solutions',
        ),
        migrations.RemoveField(
            model_name='member',
            name='themes',
        ),
        migrations.RemoveField(
            model_name='member',
            name='themes_duration',
        ),
        migrations.AddField(
            model_name='theme',
            name='description',
            field=models.TextField(default='', max_length=10000, verbose_name='Подробное описание'),
        ),
        migrations.AddField(
            model_name='theme',
            name='is_current',
            field=models.BooleanField(default=False, verbose_name='Является ли тема активной'),
        ),
    ]
