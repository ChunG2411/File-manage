from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core import validators

from .managers import CustomUserManager
from manage_file.config import type_user, status_request
import uuid
import os

# Create your models here.


def file_upload_to(instance, filename):
    name, extension = os.path.splitext(filename)
    upload_path = os.path.join(instance.user.username + '/avatar', name + extension)
    return upload_path


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(max_length=100, unique=True, validators=[username_validator], default=uuid.uuid4)
    email_validator = validators.validate_email
    email = models.EmailField(unique=True, validators=[email_validator])

    USERNAME_FIELD = 'username'
    objects = CustomUserManager()
    
    class Meta:
        db_table = 'tb_user'
        verbose_name = 'Người dùng'


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Profile_user')
    fullname = models.CharField(max_length=100, default='')
    avatar = models.ImageField(upload_to=file_upload_to, null=True, blank=True,  default='user.png')
    type = models.CharField(choices=type_user, max_length=10, default='1')
    store = models.IntegerField(default=1000) #1Gb
    limit_upload = models.IntegerField(default=5)
    limit_download = models.IntegerField(default=5)

    class Meta:
        db_table = 'tb_profile'
        verbose_name = 'Thông tin người dùng'


class LimitAction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='LimitAction_user')
    upload = models.IntegerField(default=0)
    download = models.IntegerField(default=0)
    store = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_limit_action'
        verbose_name = 'Giới hạn hoạt động'


class RequestUpgrate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='RequestUpgrate_user')
    status = models.CharField(choices=status_request, max_length=10, default='0')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'tb_request'
        verbose_name = 'Yêu cầu nâng cấp'
        ordering = ['-created_at']
