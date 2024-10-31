from app.config.bindings import inject
from app.models.config import Config
from app.routers.router_wrapper import RouterWrapper
from app.services.config.config_service import ConfigService


class ConfigRouter(RouterWrapper):
    @inject
    def __init__(self, config_service: ConfigService):
        super().__init__(prefix=f"/config")
        self.config_service = config_service
        self.notification_service = notification_service


    def _define_routes(self):
        @self.router.post("/")
        def create_config(config: Config) -> Config:
            return self.config_service.create_config(config)


        @self.router.get("/")
        def get_config() -> Config:
            return self.config_service.get_config()


        @self.router.delete("/")
        def delete_config() -> Config:
            return self.config_service.delete_config()
