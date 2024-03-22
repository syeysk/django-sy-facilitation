# Generated by Django 4.2.1 on 2024-03-22 12:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('faci', '0003_alter_member_faci_canvas'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParkedThoughts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_create', models.DateTimeField(auto_now_add=True)),
                ('dt_modify', models.DateTimeField(auto_now_add=True)),
                ('parked_thought', models.CharField(max_length=500, verbose_name='Паркованная мысль')),
                ('faci', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faci.facicanvas')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]