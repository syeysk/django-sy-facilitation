# Generated by Django 4.2.1 on 2024-03-23 22:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('faci', '0008_keythought'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facicanvas',
            name='key_thoughts',
        ),
    ]