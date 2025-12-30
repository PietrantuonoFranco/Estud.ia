from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db

from ..security.auth import authenticate_user
from ..security.token import create_access_token

from ..schemas.user_schema import UserCreate, UserOut

from ..crud.user_crud import get_user_by_email, create_user

# Creamos el router para agrupar estas rutas
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Verificar credenciales (usando la lógica que ya tenemos)
    user = authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")
    
    # 2. Crear el token
    access_token = create_access_token(data={"sub": user.email})
    
    # 3. Devolver el token al cliente
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(form_data: UserCreate, db: Session = Depends(get_db)):
    # 1. Verificar si el usuario ya existe
    existing_user = get_user_by_email(db, form_data.email)

    if existing_user:
        raise HTTPException(
            status_code=400, 
            detail="El correo electrónico ya está registrado"
        )

    # 2. Crear instancia del usuario (create_user maneja el hash de la contraseña)
    new_user = create_user(db, form_data)
    
    # 3. Crear el token
    access_token = create_access_token(data={"sub": new_user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}