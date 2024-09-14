from typing import List

from app.clients.auth_client import AuthClient
from app.config.bindings import inject
from app.models.mail import Mail
from app.routers.router_wrapper import RouterWrapper
from app.services.mail.mail_service import MailService


class MailRouter(RouterWrapper):
    @inject
    def __init__(self, mail_service: MailService):
        super().__init__(prefix=f"/mail")
        self.mail_service = mail_service


    def _define_routes(self):
        @self.router.post("/send")
        def send_mail(mail: Mail) -> Mail:
            return self.mail_service.send_mail(mail)


        @self.router.post("/bulk-send")
        def send_bulk_mail(mails: List[Mail]) -> List[Mail]:
            return [self.mail_service.send_mail(mail) for mail in mails]
