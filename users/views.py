from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers  import RegisterSerializer, TelegramChatIDSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []


class SetTelegramChatIDView(APIView):
    """
    Эндпоинт для Telegram-бота: сохраняет chat_id пользователя.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        chat_id = request.data.get('telegram_chat_id')

        if not chat_id:
            return Response(
                {'detail': 'Необходимо передать telegram_chat_id.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        user.telegram_chat_id = chat_id
        user.save(update_fields=['telegram_chat_id'])

        serializer = TelegramChatIDSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)