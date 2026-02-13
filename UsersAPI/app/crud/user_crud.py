from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import secrets

from ..security.password import hash_password

from ..schemas.user_schema import UserCreate
from ..schemas.notebook_schema import NotebookCreate

from ..models.user_model import User
from ..models.notebook_model import Notebook


async def create_user(db: AsyncSession, user: UserCreate):
    # Encriptamos la contraseña antes de crear el objeto del modelo
    hashed_pwd = hash_password(user.password)
    
    db_user = User(
        email=user.email,
        name=user.name,
        lastname=user.lastname,
        password=hashed_pwd, # Guardamos el hash, no la clave real
        profile_image_url=str(user.profile_image_url) if user.profile_image_url else None
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user

async def create_user_from_google(db: AsyncSession, user_info: dict):
    # Google suele enviar 'given_name' y 'family_name'
    # Si no vienen, intentamos separar el 'name' completo
    full_name = user_info.get('name', '')
    first_name = user_info.get('given_name', full_name.split()[0] if full_name else 'Google')
    last_name = user_info.get('family_name', full_name.split()[-1] if len(full_name.split()) > 1 else 'User')

    new_user = User(
        email=user_info['email'],
        name=first_name,
        lastname=last_name,
        # Como tu DB no permite password nulo, generamos una cadena aleatoria
        # Esto evita que alguien pueda "adivinar" la contraseña de una cuenta de Google
        password=f"oauth_{secrets.token_hex(16)}", 
        profile_image_url=user_info.get('picture')
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    query = select(User).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def get_user(db: AsyncSession, user_id: int):
    query = select(User).filter(User.id == user_id)
    result = await db.execute(query)
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str):
    query = select(User).filter(User.email == email)
    result = await db.execute(query)
    return result.scalars().first()

# --- OPERACIONES DE NOTEBOOK ---

async def get_notebooks_by_user(db: AsyncSession, user_id: int):
    query = select(Notebook).filter(Notebook.users_id == user_id)
    result = await db.execute(query)
    return result.scalars().all()

async def create_user_notebook(db: AsyncSession, notebook: NotebookCreate):
    db_notebook = Notebook(**notebook.dict())
    db.add(db_notebook)
    await db.commit()
    await db.refresh(db_notebook)
    return db_notebook

# --- OPERACIONES DE ELIMINACIÓN ---

async def delete_user(db: AsyncSession, user_id: int):
    db_user = await get_user(db, user_id)
    if db_user:
        await db.delete(db_user)
        await db.commit()
    return db_user