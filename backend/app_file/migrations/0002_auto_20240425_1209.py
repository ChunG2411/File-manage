# Generated by Django 3.2.8 on 2024-04-25 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_file', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='saved',
        ),
        migrations.RemoveField(
            model_name='folder',
            name='saved',
        ),
    ]
