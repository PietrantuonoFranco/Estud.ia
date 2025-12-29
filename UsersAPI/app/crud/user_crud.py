from sqlalchemy.orm import Session
from ..security.password import hash_password  # Importamos la función de hash_password

from ..schemas.user_schema import UserCreate
from ..schemas.notebook_schema import NotebookCreate

from ..models.user_model import User
from ..models.notebook_model import Notebook


def create_user(db: Session, user: UserCreate):
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

def get_all_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# --- OPERACIONES DE NOTEBOOK ---

def get_notebooks_by_user(db: Session, user_id: int):
    return db.query(Notebook).filter(Notebook.users_id == user_id).all()

def create_user_notebook(db: Session, notebook: NotebookCreate):
    db_notebook = Notebook(**notebook.dict())
    db.add(db_notebook)
    db.commit()
    db.refresh(db_notebook)
    return db_notebook

# --- OPERACIONES DE ELIMINACIÓN ---

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user