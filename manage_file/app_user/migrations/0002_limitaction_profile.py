# Generated by Django 3.2.8 on 2024-04-22 10:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('type', models.CharField(choices=[('0', 'Admin'), ('1', 'User basic'), ('2', 'User prenium')], default='1', max_length=10)),
                ('store', models.IntegerField(default=1000)),
                ('limit_upload', models.IntegerField(default=5)),
                ('limit_download', models.IntegerField(default=5)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Profile_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Thông tin người dùng',
                'db_table': 'tb_profile',
            },
        ),
        migrations.CreateModel(
            name='LimitAction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('upload', models.IntegerField(default=0)),
                ('download', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='LimitAction_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Giới hạn hoạt động',
                'db_table': 'tb_limit_action',
            },
        ),
    ]