import io

from PIL import Image

from app.config.bindings import inject
from app.models.notification import Notification
from app.routers.router_wrapper import RouterWrapper
from app.services.notification.notification_service import NotificationService

width, height = 1000, 500
white_image = Image.new("RGB", (width, height), "white")

byte_array = io.BytesIO()
white_image.save(byte_array, format='PNG')
image_bytes = byte_array.getvalue()

# This is just a test router to send a notification
class TestNotificationRouter(RouterWrapper):
    @inject
    def __init__(self, notification_service: NotificationService):
        super().__init__(prefix=f"/test-notification")
        self.notification_service = notification_service


    def _define_routes(self):
        @self.router.post("/")
        def post_notification():
            return self.notification_service.send_notification(Notification(title="test notification", priority="5", file=image_bytes))
