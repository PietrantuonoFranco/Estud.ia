from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # Carga variables desde .env si existe y permite valores extra sin fallar
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Usamos las variables definidas en docker-compose (POSTGRES_*) y damos defaults razonables para local
    DB_USER: str = Field(default="user", env="POSTGRES_USER")
    DB_PASSWORD: str = Field(default="password", env="POSTGRES_PASSWORD")
    DB_NAME: str = Field(default="users_db", env="POSTGRES_DB")
    DB_PORT: int = Field(default=5432, env="POSTGRES_PORT")
    DB_HOST: str = Field(default="postgres", env="POSTGRES_HOST")
    SECRET_KEY: str = Field(default="your-secret-key-change-in-production", env="SECRET_KEY")
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

conf = Settings()