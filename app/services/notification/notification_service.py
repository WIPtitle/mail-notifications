from abc import ABC, abstractmethod

from app.models.notification import Notification


class NotificationService(ABC):
    @abstractmethod
    def send_notification(self, notification: Notification) -> bool:
        pass
