from abc import ABC, abstractmethod

from app.models.notification import Notification
from app.models.ntfy_credentials import NtfyCredentials


class NotificationService(ABC):
    @abstractmethod
    def send_notification(self, notification: Notification) -> bool:
        pass

    @abstractmethod
    def get_ntfy_credentials(self) -> NtfyCredentials:
        pass

    @abstractmethod
    def update_ntfy_credentials(self) -> NtfyCredentials:
        pass