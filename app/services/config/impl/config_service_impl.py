import smtplib

from app.exceptions.validation_exception import ValidationException
from app.models.config import Config
from app.repositories.config.config_repository import ConfigRepository
from app.services.config.config_service import ConfigService


def validate_smtp_connection(config: Config) -> bool:
    try:
        server = smtplib.SMTP(config.smtp_server, config.smtp_port)
        server.starttls()
        server.login(config.smtp_user, config.smtp_password)
        server.quit()
        return True
    except smtplib.SMTPAuthenticationError:
        return False


class ConfigServiceImpl(ConfigService):
    def __init__(self, config_repository: ConfigRepository):
        self.config_repository = config_repository


    def get_config(self) -> Config:
        return self.config_repository.get_config()


    def create_config(self, config: Config) -> Config:
        if not validate_smtp_connection(config):
            raise ValidationException("Connection to smtp server cannot be established")
        return self.config_repository.create_config(config)


    def update_config(self, config: Config) -> Config:
        if not validate_smtp_connection(config):
            raise ValidationException("Connection to smtp server cannot be established")
        return self.config_repository.update_config(config)
