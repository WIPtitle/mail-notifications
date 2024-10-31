import os

import requests

from app.models.notification import Notification
from app.repositories.config.config_repository import ConfigRepository
from app.services.notification.notification_service import NotificationService


class ConfigServiceImpl(NotificationService):
    def __init__(self, config_repository: ConfigRepository):
        self.config_repository = config_repository
        self.ntfy_hostname = os.getenv("NTFY_HOSTNAME")


    def send_notification(self, notification: Notification) -> bool:
        config = self.config_repository.get_config()

        url = f"http://{self.ntfy_hostname}/{config.alarm_topic}"
        payload = {"message": notification.text}
        response = requests.post(url, json=payload)

        return response.status_code == 200
