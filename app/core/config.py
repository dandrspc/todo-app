from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    DATABASE_URL: str = f'sqlite:///{BASE_DIR}/todosapp.db'

    SECRET_KEY: str = 'supersecretkey-not-a-good-one-for-production'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 3600

    ENVIRONMENT: str = 'development'

    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, '.env'),
        extra='ignore'
    )

settings = Settings()
