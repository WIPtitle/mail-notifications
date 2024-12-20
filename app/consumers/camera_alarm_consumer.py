from typing import Type

from rabbitmq_sdk.consumer.base_consumer import BaseConsumer
from rabbitmq_sdk.enums.event import Event
from rabbitmq_sdk.event.base_event import BaseEvent
from rabbitmq_sdk.event.impl.devices_manager.camera_alarm import CameraAlarm

from app.models.notification import Notification
from app.services.notification.notification_service import NotificationService


class CameraAlarmConsumer(BaseConsumer):
    def __init__(self, notification_service: NotificationService):
        super().__init__()
        self.notification_service = notification_service

    def get_event(self) -> Event:
        return Event.CAMERA_ALARM

    def event_class(self) -> Type[BaseEvent]:
        return CameraAlarm

    def do_handle(self, event):
        event: CameraAlarm = CameraAlarm.from_dict(event)
        self.notification_service.send_notification(
            Notification(
                title="[ALARM TRIGGERED] Camera: " + event.name,
                priority="5",
                file=event.blob
            )
        )