from typing import Type

from rabbitmq_sdk.consumer.base_consumer import BaseConsumer
from rabbitmq_sdk.enums.event import Event
from rabbitmq_sdk.event.base_event import BaseEvent
from rabbitmq_sdk.event.impl.devices_manager.reed_alarm import ReedAlarm


class ReedAlarmConsumer(BaseConsumer):
    def __init__(self):
        super().__init__()

    def get_event(self) -> Event:
        return Event.REED_ALARM

    def event_class(self) -> Type[BaseEvent]:
        return ReedAlarm

    def do_handle(self, event):
        event: ReedAlarm = ReedAlarm.from_dict(event)
        #TODO emit notification