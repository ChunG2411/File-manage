from django.db import models
from app_user.models import User
from manage_file.config import permissions
import uuid
import os

# Create your models here.


def file_upload_to(instance, filename):
    _, extension = os.path.splitext(filename)
    path = instance.created_by.username + '/upload'
    if instance.parent:
        path += '/' + str(instance.parent.id)

    upload_path = os.path.join(path, instance.name.rsplit('.', 1)[0] + extension)
    return upload_path


class Folder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, default='New folder')
    description = models.CharField(max_length=100, default='')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    permissions = models.CharField(max_length=10, choices=permissions, default='0')
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tb_folder'
        verbose_name = 'Thư mục'


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, default='New file')
    description = models.CharField(max_length=100, default='')
    file = models.FileField(upload_to=file_upload_to)
    size = models.IntegerField(default=0)
    parent = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    permissions = models.CharField(max_length=10, choices=permissions, default='0')
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tb_file'
        verbose_name = 'Tập tin'
    
    def delete(self, *args, **kwargs):
        storage, path = self.file.storage, self.file.path
        super(File, self).delete(*args, **kwargs)
        storage.delete(path)


class Saved(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    folder = models.ManyToManyField(Folder, null=True, related_name="Saved_folder")
    file = models.ManyToManyField(File, null=True, related_name="Saved_file")

    class Meta:
        db_table = 'tb_saved'
        verbose_name = 'Đã lưu'