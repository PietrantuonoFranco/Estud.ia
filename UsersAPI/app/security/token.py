import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..config import conf
from ..models.user_model import User

# Este es el endpoint donde el usuario enviará su user/pass para obtener el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    """Genera un JWT firmado."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=conf.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, conf.SECRET_KEY, algorithm=conf.ALGORITHM)
    return encoded_jwt

def verify_token(token: str, db: Session):
    """
    Decodifica el token, valida su integridad y verifica 
    que el usuario exista en la base de datos.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 1. Decodificar el token
        payload = jwt.decode(token, conf.SECRET_KEY, algorithms=[conf.ALGORITHM])
        email: str = payload.get("sub") # 'sub' es el estándar para el sujeto (email)
        
        if email is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception

    # 2. Buscar al usuario en la DB para asegurar que sigue activo/existe
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
        
    return user