from abc import ABC, abstractmethod
class NotificationChannel(ABC):
    @abstractmethod
    def send(self, subject: str, body: str): ...
