import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

load_dotenv()


class DataBaseSettings(BaseSettings):
    """
    Установка полей для базы данных
    DB_USER: имя пользователя
    DB_PASS: пароль
    DB_HOST: хост
    DB_PORT: порт
    DB_NAME: имя БД
    url: драйвер для бд
    echo: вывод в консоль запросов в бд
    """

    DB_USER: str = str(os.getenv("DB_USER"))
    DB_PASS: str = str(os.getenv("DB_PASS"))
    DB_HOST: str = str(os.getenv("DB_HOST"))
    DB_PORT: int = int(os.getenv("DB_PORT"))
    DB_NAME: str = str(os.getenv("DB_NAME"))
    echo: bool = False

    @property
    def database_url_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_NAME}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


setting_database = DataBaseSettings()

engine = create_async_engine(
    url=setting_database.database_url_asyncpg, echo=setting_database.echo
)

session_maker = async_sessionmaker(bind=engine)
