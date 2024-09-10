from abc import ABC, abstractmethod

from app.models.config import Config
from app.models.mail import Mail


class MailRepository(ABC):
    @abstractmethod
    def send_mail(self, mail: Mail, config: Config):
        pass