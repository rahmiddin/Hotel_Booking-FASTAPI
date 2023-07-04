from typing import Literal

from pydantic import BaseSettings


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    DB_HOST_TEST: str
    DB_PORT_TEST: str
    DB_USER_TEST: str
    DB_PASS_TEST: str
    DB_NAME_TEST: str

    SECRET: str
    TOKEN_ALGORITHM: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def get_database_url(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}' \
               f'@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def get_test_database_url(self):
        return f'postgresql+asyncpg://{self.DB_USER_TEST}:{self.DB_PASS_TEST}' \
               f'@{self.DB_HOST_TEST}:{self.DB_PORT_TEST}/{self.DB_NAME_TEST}'

    class Config:
        env_file = ".env"


settings = Settings()
