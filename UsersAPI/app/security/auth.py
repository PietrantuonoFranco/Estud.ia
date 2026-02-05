from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session


from ..database import get_db

from ..crud.user_crud import get_user_by_email

from .token import verify_token
from .password import verify_password



async def authenticate_user(db: Session, email: str, password_plana: str):
    user = await get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password_plana, user.password):
        return False
    return user

# Dependencia para obtener el usuario desde la cookie
async def get_current_user(accessToken: str = Cookie(alias="accessToken", default=None), db: Session = Depends(get_db)):
    if not accessToken:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token no encontrado")
    
    user = verify_token(accessToken, db)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    
    return user