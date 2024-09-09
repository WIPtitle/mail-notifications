from functools import wraps
from typing import Callable, get_type_hints

from app.database.database_connector import DatabaseConnector
from app.database.impl.database_connector_impl import DatabaseConnectorImpl
from app.services.mail.impl.mail_service_impl import MailServiceImpl
from app.services.mail.mail_service import MailService

bindings = { }

# Create instances only one time
database_connector = DatabaseConnectorImpl()

mail_service = MailServiceImpl()

# Put them in an interface -> instance dict so they will be used everytime a dependency is required
bindings[DatabaseConnector] = database_connector

bindings[MailService] = mail_service


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