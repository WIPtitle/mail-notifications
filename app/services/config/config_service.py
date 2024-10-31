from abc import ABC, abstractmethod

from app.models.config import Config


class ConfigService(ABC):
    @abstractmethod
    def get_config(self) -> Config:
        pass

    @abstractmethod
    def create_config(self, config: Config) -> Config:
        pass

    @abstractmethod
    def delete_config(self) -> Config:
        pass
