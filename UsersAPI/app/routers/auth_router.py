from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..security.auth import authenticate_user
from ..security.token import create_access_token


# Creamos el router para agrupar estas rutas
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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