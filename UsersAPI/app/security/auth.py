from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db

from ..models.user_model import User

from ..crud.user_crud import get_user_by_email

from .token import verify_token, oauth2_scheme
from .password import verify_password

async def authenticate_user(db: Session, email: str, password_plana: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password_plana, user.password):
        return False
    return user

# 1. Dependencia para obtener el usuario autenticado
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = verify_token(token, db) # Función que valida el JWT

    if not user:
        raise HTTPException(status_code=401, detail="Token inválido")
    return user