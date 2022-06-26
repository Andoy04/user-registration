
import email
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.password_validation import validate_password



from .models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'is_active')
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_active=False,
            password=validated_data['password']
        )

        user.save()

        return user