# Generated by Django 4.2.1 on 2024-03-24 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faci', '0011_remove_member_counter_offer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theme',
            name='description',
            field=models.TextField(max_length=10000, verbose_name='Подробное описание'),
        ),
    ]
