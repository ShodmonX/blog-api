import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str
    VERSION: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    DATABASE_URL: str
    DEBUG: bool
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    
    model_config = SettingsConfigDict(env_file=os.getenv("ENV_FILE", ".env"), env_file_encoding="utf-8")

settings = Settings()