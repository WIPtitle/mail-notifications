import sys
import asyncio
from typing import Type

from rabbitmq_sdk.consumer.base_consumer import BaseConsumer
from rabbitmq_sdk.enums.event import Event
from rabbitmq_sdk.event.base_event import BaseEvent
from rabbitmq_sdk.event.impl.devices_manager.camera_alarm import CameraAlarm

from app.clients.auth_client import AuthClient
from app.models.mail import Mail
from app.services.mail.mail_service import MailService


class CameraAlarmConsumer(BaseConsumer):
    def __init__(self, mail_service: MailService, auth_client: AuthClient):
        super().__init__()
        self.mail_service = mail_service
        self.auth_client = auth_client

    def get_event(self) -> Event:
        return Event.CAMERA_ALARM

    def event_class(self) -> Type[BaseEvent]:
        return CameraAlarm

    def do_handle(self, event):
        event: CameraAlarm = CameraAlarm.from_dict(event)
        print("should send email")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop = asyncio.get_event_loop()
        users = loop.run_until_complete(self.auth_client.get_all_users())
        print(users)
        sys.stdout.flush()
        try:
            self.mail_service.send_mail(
                Mail(
                    receiver="",
                    subject="",
                    text=""
                )
            )
        except:
            pass