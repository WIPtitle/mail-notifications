import os
from functools import wraps
from typing import Callable, get_type_hints

from rabbitmq_sdk.client.impl.rabbitmq_client_impl import RabbitMQClientImpl
from rabbitmq_sdk.enums.service import Service

from app.consumers.camera_alarm_consumer import CameraAlarmConsumer
from app.consumers.reed_alarm_consumer import ReedAlarmConsumer
from app.database.database_connector import DatabaseConnector
from app.database.impl.database_connector_impl import DatabaseConnectorImpl
from app.repositories.config.impl.config_repository_impl import ConfigRepositoryImpl
from app.services.config.config_service import ConfigService
from app.services.config.impl.config_service_impl import ConfigServiceImpl
from app.services.notification.impl.notification_service_impl import NotificationServiceImpl
from app.services.notification.notification_service import NotificationService
from app.utils.read_credentials import read_credentials

bindings = { }

database_connector = DatabaseConnectorImpl()

rabbit_credentials = read_credentials(os.getenv('RBBT_CREDENTIALS_FILE'))
rabbitmq_client = RabbitMQClientImpl.from_config(
    host=os.getenv("RABBITMQ_HOSTNAME"), # using container name as host instead of ip
    port=5672,
    username=rabbit_credentials['RABBITMQ_USER'],
    password=rabbit_credentials['RABBITMQ_PASSWORD']
).with_current_service(Service.MAIL_NOTIFICATION)


# Create instances only one time
config_repository = ConfigRepositoryImpl(database_connector=database_connector)

config_service = ConfigServiceImpl(config_repository)
notification_service = NotificationServiceImpl(config_repository)

# Consumers
reed_alarm_consumer = ReedAlarmConsumer()
camera_alarm_consumer = CameraAlarmConsumer()

rabbitmq_client.consume(camera_alarm_consumer)
rabbitmq_client.consume(reed_alarm_consumer)

# Put them in an interface -> instance dict so they will be used everytime a dependency is required
bindings[DatabaseConnector] = database_connector

bindings[ConfigService] = config_service
bindings[NotificationService] = notification_service


def resolve(interface):
    implementation = bindings[interface]
    if implementation is None:
        raise ValueError(f"No binding found for {interface}")
    return implementation


def inject(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        type_hints = get_type_hints(func)
        for name, param_type in type_hints.items():
            if param_type in bindings:
                kwargs[name] = resolve(param_type)
        return func(*args, **kwargs)
    return wrapper