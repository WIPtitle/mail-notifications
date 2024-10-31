import os

import requests

from io import BytesIO

from PIL import Image

from app.models.notification import Notification
from app.repositories.config.config_repository import ConfigRepository
from app.services.notification.notification_service import NotificationService


class NotificationServiceImpl(NotificationService):
    def __init__(self, config_repository: ConfigRepository):
        self.config_repository = config_repository
        self.ntfy_hostname = os.getenv("NTFY_HOSTNAME")


    def send_notification(self, notification: Notification) -> bool:
        config = self.config_repository.get_config()
        url = f"http://{self.ntfy_hostname}/{config.alarm_topic}"

        if notification.file is not None:
            blob = notification.file
            image = Image.open(BytesIO(blob))
            byte_io = BytesIO()
            image.save(byte_io, 'JPEG')
            byte_io.seek(0)

            headers = {
                "Title": notification.title,
                "Priority": notification.priority,
                "Filename": "image.jpeg",
                "Actions": f"view, Open webpage, {notification.url}, clear=true",
            }

            response = requests.post(url, data=byte_io.getvalue(), headers=headers)
        else:
            headers = {
                "Title": notification.title,
                "Priority": notification.priority,
                "Actions": f"view, Open webpage, {notification.url}, clear=true",
            }

            response = requests.post(url, headers=headers)

        return response.status_code == 200
