import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.exceptions.bad_request_exception import BadRequestException
from app.models.config import Config
from app.models.mail import Mail
from app.repositories.mail.mail_repository import MailRepository


class MailRepositoryImpl(MailRepository):
    def send_mail(self, mail: Mail, config: Config):
        try:
            server = smtplib.SMTP(config.smtp_server, config.smtp_port)
            server.starttls()
            server.login(config.smtp_user, config.smtp_password)

            msg = MIMEMultipart()
            msg['From'] = config.email_from
            msg['To'] = mail.receiver
            msg['Subject'] = mail.subject
            msg.attach(MIMEText(mail.text, 'plain'))

            server.send_message(msg)
            server.quit()
            return mail
        except smtplib.SMTPException:
            raise BadRequestException("Email can't be sent, is configuration valid?")