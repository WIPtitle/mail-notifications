import os

import requests

from io import BytesIO

from PIL import Image

from app.models.notification import Notification
from app.services.notification.notification_service import NotificationService
from app.utils.read_credentials import read_credentials


class NotificationServiceImpl(NotificationService):
    def __init__(self):
        self.ntfy_hostname = os.getenv("NTFY_HOSTNAME")
        self.ntfy_credentials = read_credentials(os.getenv('NTFY_CREDENTIALS_FILE'))


    def send_notification(self, notification: Notification) -> bool:
        url = f"http://{self.ntfy_hostname}/{self.ntfy_credentials['NTFY_TOPIC']}"
        auth = (self.ntfy_credentials['NTFY_WRITER_USER'], self.ntfy_credentials['NTFY_WRITER_PASSWORD'])

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

            response = requests.post(url, data=byte_io.getvalue(), headers=headers, auth=auth)
        else:
            headers = {
                "Title": notification.title,
                "Priority": notification.priority,
                "Actions": f"view, Open webpage, {notification.url}, clear=true",
            }

            response = requests.post(url, headers=headers, auth=auth)

        return response.status_code == 200
