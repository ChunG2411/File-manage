# Generated by Django 5.0.4 on 2024-05-13 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0008_emailcode_alter_requestupgrate_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='status',
        ),
    ]