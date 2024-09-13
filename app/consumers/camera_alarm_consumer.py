from typing import Type

from rabbitmq_sdk.consumer.base_consumer import BaseConsumer
from rabbitmq_sdk.enums.event import Event
from rabbitmq_sdk.event.base_event import BaseEvent
from rabbitmq_sdk.event.impl.devices_manager.camera_alarm import CameraAlarm

from app.models.mail import Mail
from app.services.mail.mail_service import MailService


class CameraAlarmConsumer(BaseConsumer):
    def __init__(self, mail_service: MailService):
        super().__init__()
        self.mail_service = mail_service

    def get_event(self) -> Event:
        return Event.CAMERA_ALARM

    def event_class(self) -> Type[BaseEvent]:
        return CameraAlarm

    def do_handle(self, event):
        event: CameraAlarm = CameraAlarm.from_dict(event)
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