import requests
from .base import NotificationChannel
from ..config import settings
class TelegramNotifier(NotificationChannel):
    def send(self, subject, body):
        if not settings.telegram_bot_token or not settings.telegram_chat_id:
            return False, "Telegram credentials not configured"
        url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
        r = requests.post(url, json={"chat_id": settings.telegram_chat_id, "text": f"{subject}\n\n{body}"}, timeout=15)
        r.raise_for_status(); return True, None
