import smtplib
from email.message import EmailMessage
from .base import NotificationChannel
from ..config import settings
class EmailNotifier(NotificationChannel):
    def __init__(self, recipient: str): self.recipient = recipient
    def send(self, subject, body):
        if not settings.smtp_host or not settings.smtp_username or not settings.smtp_password or not settings.smtp_from:
            return False, "SMTP credentials not configured"
        msg = EmailMessage(); msg["From"] = settings.smtp_from; msg["To"] = self.recipient; msg["Subject"] = subject; msg.set_content(body)
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as s:
            s.starttls(); s.login(settings.smtp_username, settings.smtp_password); s.send_message(msg)
        return True, None
