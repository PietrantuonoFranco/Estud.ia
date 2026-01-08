from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # Configuración para buscar el archivo .env si no existen variables de sistema
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

    DB_USER: str = Field(..., validation_alias="POSTGRES_USER")
    DB_PASSWORD: str = Field(..., validation_alias="POSTGRES_PASSWORD")
    DB_NAME: str = Field(..., validation_alias="POSTGRES_DB")
    DB_PORT: int = Field(..., validation_alias="POSTGRES_PORT")
    DB_HOST: str = Field(..., validation_alias="POSTGRES_HOST")
    
    SECRET_KEY: str = Field(..., validation_alias="SECRET_KEY")
    ALGORITHM: str = Field(..., validation_alias="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(..., validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    LANGCHAIN_URI: str = Field(..., validation_alias="LANGCHAIN_URI")
    LANGCHAIN_API_KEY: str = Field(..., validation_alias="LANGCHAIN_API_KEY")

conf = Settings()