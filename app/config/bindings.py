from functools import wraps
from typing import Callable, get_type_hints

from app.repositories.config.impl.config_repository_impl import ConfigRepositoryImpl
from app.repositories.mail.impl.mail_repository_impl import MailRepositoryImpl
from app.services.config.config_service import ConfigService
from app.services.config.impl.config_service_impl import ConfigServiceImpl
from app.services.mail.impl.mail_service_impl import MailServiceImpl
from app.services.mail.mail_service import MailService

bindings = { }

# Create instances only one time
mail_repository = MailRepositoryImpl()
config_repository = ConfigRepositoryImpl()

mail_service = MailServiceImpl(config_repository, mail_repository)
config_service = ConfigServiceImpl(config_repository)

# Put them in an interface -> instance dict so they will be used everytime a dependency is required
bindings[MailService] = mail_service
bindings[ConfigService] = config_service


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