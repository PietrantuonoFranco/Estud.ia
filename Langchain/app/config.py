from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # Configuración para buscar el archivo .env si no existen variables de sistema
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )
    
    API_KEY_NAME: str = Field(..., validation_alias="API_KEY_NAME")

    GOOGLE_API_KEY: str = Field(..., validation_alias="GOOGLE_API_KEY")
    VOYAGE_API_KEY: str = Field(..., validation_alias="VOYAGE_API_KEY")

    # Configuración para Zilliz (Producción)
    ZILLIZ_TOKEN: Optional[str] = Field(default=None, validation_alias="ZILLIZ_TOKEN")
    ZILLIZ_URI: Optional[str] = Field(default=None, validation_alias="ZILLIZ_URI")
    
    # Configuración para Milvus (Desarrollo)
    MILVUS_URI: Optional[str] = Field(default=None, validation_alias="MILVUS_URI")

conf = Settings()