import os

from fastapi.security import HTTPBearer
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

HTTP_BEARER = HTTPBearer(auto_error=False)


class DataBaseSettings(BaseSettings):
    """
    Установка полей для базы данных
    url - драйвер для бд
    echo - вывод в консоль запросов в бд
    """

    model_config = SettingsConfigDict(env_file="../../../.env")

    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    echo: bool = False

    @property
    def database_url_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_NAME}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


setting_database = DataBaseSettings()  # noqa

engine = create_async_engine(
    url=setting_database.database_url_asyncpg, echo=setting_database.echo
)

session_maker = async_sessionmaker(bind=engine)
