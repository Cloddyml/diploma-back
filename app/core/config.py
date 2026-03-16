from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    MODE: Literal["TEST", "LOCAL", "DEV", "PROD"]

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int

    API_VERSION: str

    QWEN_API_KEY: str
    QWEN_MODEL: str
    QWEN_BASE_URL: str
    QWEN_TEMP: float
    QWEN_MAX_TOKENS: int

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def SYNC_DB_URL(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def REDIS_BROKER_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/1"

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env.local", extra="ignore")


settings = Settings()  # pyright: ignore[reportCallIssue]
