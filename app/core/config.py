# app/core/config.py

from pydantic import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "sghss"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "123456"  # ou a senha que você definiu


    class Config:
        env_file = ".env"

settings = Settings()
