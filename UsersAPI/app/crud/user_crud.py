from sqlalchemy.orm import Session
import secrets

from ..security.password import hash_password

from ..schemas.user_schema import UserCreate
from ..schemas.notebook_schema import NotebookCreate

from ..models.user_model import User
from ..models.notebook_model import Notebook


async def create_user(db: Session, user: UserCreate):
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
    db.commit()
    db.refresh(db_user)

    return db_user

async def create_user_from_google(db: Session, user_info: dict):
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
    db.commit()
    db.refresh(new_user)
    return new_user

async def get_all_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

async def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

async def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# --- OPERACIONES DE NOTEBOOK ---

async def get_notebooks_by_user(db: Session, user_id: int):
    return db.query(Notebook).filter(Notebook.users_id == user_id).all()

async def create_user_notebook(db: Session, notebook: NotebookCreate):
    db_notebook = Notebook(**notebook.dict())
    db.add(db_notebook)
    db.commit()
    db.refresh(db_notebook)
    return db_notebook

# --- OPERACIONES DE ELIMINACIÓN ---

async def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user