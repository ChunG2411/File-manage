# Generated by Django 5.0.4 on 2024-05-10 04:49

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0005_limitaction_store'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestupgrate',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='type',
            field=models.CharField(choices=[('0', 'Admin'), ('1', 'User')], default='1', max_length=10),
        ),
    ]