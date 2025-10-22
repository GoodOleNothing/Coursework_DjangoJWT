# habits/telegram_client.py
import requests
from django.conf import settings

BASE_URL = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}"


def send_telegram_message_request(chat_id: int, text: str) -> bool:
    """
    Отправляет сообщение пользователю Telegram через API методом POST.
    Возвращает True, если сообщение успешно отправлено.
    """
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 200:
            return True
        else:
            print(f"[Telegram Error] {response.status_code}: {response.text}")
            return False
    except requests.RequestException as e:
        print(f"[Telegram Exception] {e}")
        return False
