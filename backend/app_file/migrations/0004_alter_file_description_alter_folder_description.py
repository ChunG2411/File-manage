# Generated by Django 5.0.4 on 2024-05-06 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_file', '0003_saved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='description',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='folder',
            name='description',
            field=models.CharField(default='', max_length=100),
        ),
    ]
