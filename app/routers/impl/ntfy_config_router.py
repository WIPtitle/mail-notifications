from app.config.bindings import inject
from app.routers.router_wrapper import RouterWrapper
from app.services.notification.notification_service import NotificationService


class NtfyConfigRouter(RouterWrapper):
    @inject
    def __init__(self, notification_service: NotificationService):
        super().__init__(prefix=f"/ntfy-config")
        self.notification_service = notification_service


    def _define_routes(self):
        @self.router.post("/credentials")
        def get_ntfy_credentials():
            return self.notification_service.get_ntfy_credentials()
