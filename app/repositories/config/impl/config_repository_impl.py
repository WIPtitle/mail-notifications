from sqlmodel import select

from app.database.database_connector import DatabaseConnector
from app.exceptions.not_found_exception import NotFoundException
from app.models.config import Config
from app.repositories.config.config_repository import ConfigRepository


class ConfigRepositoryImpl(ConfigRepository):
    def __init__(self, database_connector: DatabaseConnector):
        self.database_connector = database_connector

    def get_config(self) -> Config:
        statement = select(Config)
        config_db = self.database_connector.get_session().exec(statement).one_or_none()
        if config_db is None:
            raise NotFoundException("Config was not found")

        return config_db


    def create_config(self, config: Config) -> Config:
        try:
            self.delete_config()
        except:
            pass
        self.database_connector.get_session().add(config)
        self.database_connector.get_session().commit()
        self.database_connector.get_session().refresh(config)
        return config


    def delete_config(self) -> Config:
        config_db = self.get_config()
        self.database_connector.get_session().delete(config_db)
        self.database_connector.get_session().commit()
        return config_db
