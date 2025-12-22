from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DB_USER = str(os.getenv("POSTGRES_USER", "usuario_por_defecto"))
    DB_PASSWORD = str(os.getenv("POSTGRES_PASSWORD", "password_por_defecto"))
    DB_NAME = str(os.getenv("POSTGRES_DB", "nombre_db"))
    DB_PORT = int(os.getenv("POSTGRES_PORT", "5432"))

    # Si la API está en Docker, el host es 'postgres'. Si es local, es 'localhost'.
    DB_HOST = str(os.getenv("POSTGRES_HOST", "postgres")) 


conf = Settings()