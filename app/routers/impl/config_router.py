from app.config.bindings import inject
from app.models.config import Config, ConfigResponse
from app.routers.router_wrapper import RouterWrapper
from app.services.config.config_service import ConfigService


class ConfigRouter(RouterWrapper):
    @inject
    def __init__(self, config_service: ConfigService):
        super().__init__(prefix=f"/config")
        self.config_service = config_service


    def _define_routes(self):
        @self.router.post("/")
        def create_config(config: Config) -> ConfigResponse:
            return ConfigResponse.model_validate(self.config_service.create_config(config))


        @self.router.get("/")
        def get_config() -> ConfigResponse:
            return ConfigResponse.model_validate(self.config_service.get_config())
