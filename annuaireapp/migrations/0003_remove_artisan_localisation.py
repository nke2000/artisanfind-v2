# Generated by Django 4.2 on 2025-06-24 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annuaireapp', '0002_contactmessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artisan',
            name='localisation',
        ),
    ]
