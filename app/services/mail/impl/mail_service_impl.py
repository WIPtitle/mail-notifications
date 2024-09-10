from app.models.mail import Mail
from app.repositories.config.config_repository import ConfigRepository
from app.repositories.mail.mail_repository import MailRepository
from app.services.mail.mail_service import MailService


class MailServiceImpl(MailService):
    def __init__(self, config_repository: ConfigRepository, mail_repository: MailRepository):
        self.config_repository = config_repository
        self.mail_repository = mail_repository

    def send_mail(self, mail: Mail) -> Mail:
        config = self.config_repository.get_config()
        return self.mail_repository.send_mail(mail, config)
