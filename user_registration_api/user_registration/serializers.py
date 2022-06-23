from rest_framework import serializers
from .models import User

class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ('email_address', 'first_name', 'last_name', 'active')