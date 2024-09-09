from abc import ABC, abstractmethod

from app.models.mail import Mail


class MailService(ABC):
    @abstractmethod
    def send_mail(self, mail: Mail) -> Mail:
        pass
