from app.models.config import Config
from app.repositories.config.config_repository import ConfigRepository
from app.services.config.config_service import ConfigService


class ConfigServiceImpl(ConfigService):
    def __init__(self, config_repository: ConfigRepository):
        self.config_repository = config_repository


    def get_config(self) -> Config:
        return self.config_repository.get_config()


    def create_config(self, config: Config) -> Config:
        return self.config_repository.create_config(config)


    def delete_config(self) -> Config:
        return self.config_repository.delete_config()