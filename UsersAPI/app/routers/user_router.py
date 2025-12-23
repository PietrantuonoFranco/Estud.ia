from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import SessionLocal
from ..models.user_model import User
from ..schemas.user_schema import UserCreate, UserOut

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
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # 2. Crear la instancia del modelo (aquí deberías hashear la password)
    new_user = User(
        email=user.email,
        name=user.name,
        lastname=user.lastname,
        password=user.password, # ¡Recuerda encriptar esto en un proyecto real!
        profile_image_url=str(user.profile_image_url) if user.profile_image_url else None
    )
    
    # 3. Guardar en la base de datos
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # Refresca para obtener el ID generado por Postgres
    
    return new_user

# RUTA 2: Obtener todos los usuarios (GET)
@router.get("/", response_model=List[UserOut])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

# RUTA 3: Obtener un usuario por ID (GET)
@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user