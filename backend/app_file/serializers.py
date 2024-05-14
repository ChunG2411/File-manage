from rest_framework import serializers

from .models import (
    Folder, File, Saved
)
from manage_file.function import get_path_url


class FolderSerializers(serializers.ModelSerializer):
    folder = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()
    path = serializers.SerializerMethodField()

    class Meta:
        model = Folder
        fields = '__all__'

    def get_folder(self, obj):
        folder = Folder.objects.filter(parent=obj.id, deleted=False)
        return [
            {
                'id': str(i.id),
                'name': i.name,
                'permissions': i.permissions,
                'delete': i.deleted
            } for i in folder
        ]
    
    def get_file(self, obj):
        file = File.objects.filter(parent=obj.id, deleted=False)
        return [
            {
                'id': str(i.id),
                'name': i.name,
                'permissions': i.permissions,
                'file': i.file.url,
                'delete': i.deleted
            } for i in file
        ]
    
    def get_path(self, obj):
        return get_path_url(obj)


class FolderDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    saved = serializers.SerializerMethodField()

    class Meta:
        model = Folder
        fields = '__all__'
    
    def get_created_by(self, obj):
        return obj.created_by.username
    
    def get_saved(self, obj):
        saved = Saved.objects.get(user=self.context['request'].user)
        return True if obj in saved.folder.all() else False


class FileSerializers(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    path = serializers.SerializerMethodField()
    saved = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = '__all__'
    
    def get_path(self, obj):
        return get_path_url(obj)
    
    def get_created_by(self, obj):
        return obj.created_by.username
    
    def get_file(self, obj):
        return obj.file.url
    
    def get_saved(self, obj):
        saved = Saved.objects.get(user=self.context['request'].user)
        return True if obj in saved.file.all() else False


class SavedSerializers(serializers.ModelSerializer):
    folder = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()

    class Meta:
        model = Saved
        fields = '__all__'

    def get_folder(self, obj):
        return [
            {
                'id': str( i.id),
                'name': i.name,
                'permissions': i.permissions,
                'delete': i.deleted
            } for i in obj.folder
        ]
    
    def get_file(self, obj):
        return [
            {
                'id': str(i.id),
                'name': i.name,
                'permissions': i.permissions,
                'file': i.file.url,
                'delete': i.deleted
            } for i in obj.file
        ]
    