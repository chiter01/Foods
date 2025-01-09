from rest_framework import serializers

from account.models import User

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from account.models import User

class LoginSerializer(serializers.Serializer):

    email = serializers.CharField()
    password = serializers.CharField()


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'get_full_name',
            'first_name',
            'last_name',
            'email',
            'phone',
            'avatar',
            'role',
        )
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ('email', 'phone', 'first_name', 'last_name', 'password', 'password_confirm', 'avatar')

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Пароли не совпадают")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            email=validated_data['email'],
            phone=validated_data['phone'],
            password=validated_data['password'],
            first_name=validated_data['first_name'], 
            last_name=validated_data['last_name'],    
            avatar=validated_data.get('avatar')       
        )
        return user
    



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError("Новые пароли не совпадают")
        return data

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Старый пароль неверен")
        return value

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

from rest_framework import serializers
from account.models import User

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

User = get_user_model() 

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'email']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance