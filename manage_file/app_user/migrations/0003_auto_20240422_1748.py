# Generated by Django 3.2.8 on 2024-04-22 10:48

import app_user.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0002_limitaction_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='user.png', null=True, upload_to=app_user.models.file_upload_to),
        ),
        migrations.AddField(
            model_name='profile',
            name='fullname',
            field=models.CharField(default='', max_length=100),
        ),
    ]