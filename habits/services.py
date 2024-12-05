import requests
from django.conf import settings


def send_telegram_message(message, tg_chat_id):
    """Отправка сообщения в Telegram через бот"""
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": tg_chat_id, "text": message}
    requests.post(url, data=data)
    print("Сообщение отправлено")
