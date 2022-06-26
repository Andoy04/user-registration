
from multiprocessing import AuthenticationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.password_validation import validate_password


from .auth import Google
import os

from .models import User

#class UserSerializer(serializers.ModelSerializer):
#    auth_token = serializers.CharField()
#
#    class Meta:
#        model = User
#        fields = ('email', 'password', 'first_name', 'last_name', 'is_active')
#        extra_kwargs = {
#            'password': {'write_only': True},
#            'is_active': {'read_only': True},
#        }
#
#    def create(self, validated_data):
#        user = User.objects.create(
#            email=validated_data['email'],
#            first_name=validated_data['first_name'],
#            last_name=validated_data['last_name'],
#            is_active=False,
#            password=validated_data['password']
#        )
#
#        user.save()
#
#        return user
#
#    def validate_auth_token(self, auth_token):
#        user = Google.validate(auth_token)
#
#        try:
#            user['sub']
#        except:
#            raise serializers.ValidationError(
#                'Expired or invalid token.'
#            )
#
#        if user['aud'] != os.environ.get('GOOGLE_CLIENT_ID'):
#            raise AuthenticationError('Failed to authenticate')
#
#        user_id = user['sub']
#        email = user['email']
#        first_name = user['first_name']
#        last_name = user['last_name']
#        provider = 'google'
#
#        user = User.objects.filter(email=email)
#        return user


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True},
        }

    def validate(self, attrs):
        email = attrs.get('email', '')

        if not email:
            raise serializers.ValidationError('no email was provided')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        extra_kwargs = {
            'password': {'write_only': True}
        }
        fields = ['token', 'password']

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')