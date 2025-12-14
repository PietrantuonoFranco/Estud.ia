import os
import secrets
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv

load_dotenv()

# Configuración de API Key
API_KEY = os.getenv("API_KEY_NAME", "default-secret-key")  # Esta es la que esta eb el .env
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False) ##Viene del header de la peticion


def verify_api_key(api_key: str = Security(api_key_header)): ##Metodo  que verifica la ApiKey

    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API Key"
        )
    return api_key


def generate_api_key(length: int = 32) -> str: ## Gebera una API Key

    return secrets.token_urlsafe(length)

print(generate_api_key())