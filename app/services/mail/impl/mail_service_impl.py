from app.models.mail import Mail
from app.services.mail.mail_service import MailService


class MailServiceImpl(MailService):

    def send_mail(self, mail: Mail) -> Mail:
        print("sending mail")
        return mail
