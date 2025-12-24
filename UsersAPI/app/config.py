from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # Carga variables desde .env si existe y permite valores extra sin fallar
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Usamos las variables definidas en docker-compose (POSTGRES_*) y damos defaults razonables para local
    DB_USER: str = Field("postgres", env="POSTGRES_USER")
    DB_PASSWORD: str = Field("postgres", env="POSTGRES_PASSWORD")
    DB_NAME: str = Field("postgres", env="POSTGRES_DB")
    DB_PORT: int = Field(5432, env="POSTGRES_PORT")
    # Por defecto local; en Docker compose se inyecta POSTGRES_HOST=postgres
    DB_HOST: str = Field("localhost", env="POSTGRES_HOST")
    
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field("HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60, env="ACCESS_TOKEN_EXPIRE_MINUTES")

conf = Settings()