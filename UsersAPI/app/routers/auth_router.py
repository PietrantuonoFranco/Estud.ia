from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..database import get_db

from ..security.auth import authenticate_user, get_current_user
from ..security.token import create_access_token

from ..schemas.user_schema import UserCreate

from ..crud.user_crud import get_user_by_email, create_user

from ..config import conf

# Creamos el router para agrupar estas rutas
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return current_user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), status_code=status.HTTP_200_OK):
    user = authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")
    
    accessToken = create_access_token(data={"sub": user.email})
    
    # Crear respuesta con cookie
    response = JSONResponse(
        content={"message": "Login exitoso", "token_type": "bearer"}
    )
    
    # Setear cookie con opciones de seguridad
    response.set_cookie(
        key="accessToken",
        value=accessToken,
        httponly=True,        # No accesible desde JavaScript
        secure=False,         # False en desarrollo, True en producción con HTTPS
        samesite="lax",      # Permite cookies cross-origin (cambiar a "Lax" en producción)
        max_age=60*conf.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    return response

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(form_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, form_data.email)

    if existing_user:
        raise HTTPException(
            status_code=400, 
            detail="El correo electrónico ya está registrado"
        )

    new_user = create_user(db, form_data)
    accessToken = create_access_token(data={"sub": new_user.email})
    
    response = JSONResponse(
        content={"message": "Registro exitoso", "token_type": "bearer"},
        status_code=status.HTTP_201_CREATED
    )
    
    response.set_cookie(
        key="accessToken",
        value=accessToken,
        httponly=True,
        secure=False,         # False en desarrollo, True en producción con HTTPS
        samesite="lax",      # Permite cookies cross-origin (cambiar a "Lax" en producción)
        max_age=60*conf.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    return response

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout():
    response = JSONResponse(content={"message": "Logout exitoso"})
    response.delete_cookie(key="accessToken")
    
    return response