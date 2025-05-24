from rest_framework import serializers
from django.contrib.auth import authenticate
from ..users.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number', 'first_name', 'last_name']

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(phone_number=data['phone_number'], password=data['password'])
        if user and user.is_active:
            return {'user': user}
        raise serializers.ValidationError("Invalid credentials")