from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        user = User.objects.create_user(
            email=email,
            password=password
        )
        return user


class TelegramChatIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['telegram_chat_id']