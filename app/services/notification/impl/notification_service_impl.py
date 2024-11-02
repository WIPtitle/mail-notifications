import os
import time

import requests

from io import BytesIO

from PIL import Image

from app.models.notification import Notification
from app.models.ntfy_credentials import NtfyCredentials
from app.services.notification.notification_service import NotificationService
from app.utils.read_credentials import read_credentials


class NotificationServiceImpl(NotificationService):
    def __init__(self):
        self.ntfy_hostname = os.getenv("NTFY_HOSTNAME") # This is the docker hostname, not the localtunnel url
        self.ntfy_credentials = read_credentials(os.getenv('NTFY_CREDENTIALS_FILE'))
        self.lt_credentials = read_credentials(os.getenv('LT_CREDENTIALS_FILE'))


    def get_ntfy_credentials(self) -> NtfyCredentials:
        return NtfyCredentials(
            user=self.ntfy_credentials['NTFY_READER_USER'],
            password=self.ntfy_credentials['NTFY_READER_PASSWORD'],
            topic=self.ntfy_credentials['NTFY_TOPIC']
        )


    def update_ntfy_credentials(self) -> NtfyCredentials:
        credentials_file = os.getenv('NTFY_CREDENTIALS_FILE')
        old_password = self.ntfy_credentials['NTFY_READER_PASSWORD']

        os.remove(credentials_file)

        new_password = old_password
        while new_password == old_password:
            time.sleep(1)
            try:
                self.ntfy_credentials = read_credentials(credentials_file)
                new_password = self.ntfy_credentials['NTFY_READER_PASSWORD']
            except FileNotFoundError:
                continue

        return NtfyCredentials(
            user=self.ntfy_credentials['NTFY_READER_USER'],
            password=self.ntfy_credentials['NTFY_READER_PASSWORD'],
            topic=self.ntfy_credentials['NTFY_TOPIC']
        )


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
                "Actions": f"view, Open webpage, {self.lt_credentials['URL_FRONTEND']}, clear=true",
            }

            response = requests.post(url, data=byte_io.getvalue(), headers=headers, auth=auth)
        else:
            headers = {
                "Title": notification.title,
                "Priority": notification.priority,
                "Actions": f"view, Open webpage, {self.lt_credentials['URL_FRONTEND']}, clear=true",
            }

            response = requests.post(url, headers=headers, auth=auth)

        return response.status_code == 200
