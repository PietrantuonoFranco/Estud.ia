from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import SessionLocal
from ..models.user_model import User
from ..schemas.user_schema import UserCreate, UserOut
from ..crud.user_crud import create_user, get_user, get_user_by_email, get_all_users


# Creamos el router para agrupar estas rutas
router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# RUTA 1: Crear un usuario (POST)
@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # 1. Verificar si el email ya existe
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    return create_user(db=db, user=user)

# RUTA 2: Obtener todos los usuarios (GET)
@router.get("/", response_model=List[UserOut])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = get_all_users(db, skip=skip, limit=limit)
    return users

# RUTA 3: Obtener un usuario por ID (GET)
@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# RUTA 4: Obtener un usuario por email (GET)
@router.get("/by_email/", response_model=UserOut)
def read_user_by_email(email: str, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# RUTA 5: Eliminar un usuario por ID (DELETE)
@router.delete("/{user_id}", response_model=UserOut)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(user)
    db.commit()
    return user