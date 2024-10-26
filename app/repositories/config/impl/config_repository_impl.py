import json
from pathlib import Path

from app.exceptions.not_found_exception import NotFoundException
from app.models.config import Config
from app.repositories.config.config_repository import ConfigRepository


class ConfigRepositoryImpl(ConfigRepository):
    def __init__(self):
        self.file_path = Path("/var/lib/mail-notifications/data/config.json")


    def get_config(self) -> Config:
        if self.file_path.exists():
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                return Config(**data)
        else:
            raise NotFoundException("Config not found")


    def create_config(self, config: Config) -> Config:
        with open(self.file_path, 'w') as file:
            json.dump(config.model_dump(), file)
        return config


    def delete_config(self) -> Config:
        if self.file_path.exists():
            with open(self.file_path, 'r') as file:
                data = json.load(file)
            self.file_path.unlink()
            return Config(**data)
        else:
            raise NotFoundException("Config not found")
