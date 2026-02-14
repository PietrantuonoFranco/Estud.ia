from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..database import get_db
from ..schemas.user_schema import UserCreate, UserOut
from ..security.auth import get_current_user
from ..utils.validate_admin import validate_admin
from ..crud.user_crud import (
    create_user as create_user_crud,
    get_user,
    get_user_by_email,
    get_all_users,
)


# Creamos el router para agrupar estas rutas
router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# RUTA 1: Crear un usuario (POST)
@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # 1. Verificar si el email ya existe
    db_user = await get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    return await create_user_crud(db=db, user=user)

# RUTA 2: Obtener todos los usuarios (GET)
@router.get("/", response_model=List[UserOut], status_code=status.HTTP_200_OK)
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    users = await get_all_users(db, skip=skip, limit=limit)
    return users

# RUTA 3: Obtener un usuario por ID (GET)
@router.get("/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# RUTA 4: Obtener un usuario por email (GET)
@router.get("/by_email/", response_model=UserOut, status_code=status.HTTP_200_OK)
async def read_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# RUTA 5: Eliminar un usuario por ID (DELETE)
@router.delete("/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user = await get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not validate_admin(current_user) and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar este usuario")

    db.delete(user)
    db.commit()
    return user