from rest_framework import serializers

from .models import (
    User, Profile, LimitAction, RequestUpgrate
)
from app_file.models import Saved

class UserRegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': 'true'}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        Profile.objects.create(user=user, fullname=user.username)
        LimitAction.objects.create(user=user)
        Saved.objects.create(user=user)
        return user


class ProfileSerializers(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'
    
    def get_user(self, obj):
        return obj.user.username
    
    def get_email(self, obj):
        return obj.user.email


class LimitActionSerializers(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = LimitAction
        fields = '__all__'
    
    def get_user(self, obj):
        return obj.user.username


class RequestUpgrateSerializers(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = RequestUpgrate
        fields = '__all__'

    def get_user(self, obj):
        return obj.user.username
    
    def get_profile(self, obj):
        profile = Profile.objects.get(user=obj.user)
        return {
            'fullname': profile.fullname,
            'email': profile.user.email,
            'avatar': profile.avatar.url,
            'type': profile.type,
        }