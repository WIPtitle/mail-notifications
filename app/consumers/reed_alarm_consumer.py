import asyncio
from typing import Type

from rabbitmq_sdk.consumer.base_consumer import BaseConsumer
from rabbitmq_sdk.enums.event import Event
from rabbitmq_sdk.event.base_event import BaseEvent
from rabbitmq_sdk.event.impl.devices_manager.reed_alarm import ReedAlarm

from app.clients.auth_client import AuthClient
from app.models.mail import Mail
from app.services.mail.mail_service import MailService


class ReedAlarmConsumer(BaseConsumer):
    def __init__(self, mail_service: MailService, auth_client: AuthClient):
        super().__init__()
        self.mail_service = mail_service
        self.auth_client = auth_client

    def get_event(self) -> Event:
        return Event.REED_ALARM

    def event_class(self) -> Type[BaseEvent]:
        return ReedAlarm

    def do_handle(self, event):
        event: ReedAlarm = ReedAlarm.from_dict(event)
        print("SENDING MAIL")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop = asyncio.get_event_loop()
        users = loop.run_until_complete(self.auth_client.get_all_users())
        try:
            for user in users:
                self.mail_service.send_mail(
                    Mail(
                        receiver=user.email,
                        subject="ALARM STARTED",
                        text=f"Your alarm has started (Magnetic reed: {event.name})",
                        attachment=None
                    )
                )
        except:
            pass