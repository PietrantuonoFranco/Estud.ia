from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional
from datetime import datetime

from .role_schema import RoleOut

# --- SCHEMAS DE USUARIO ---

class UserBase(BaseModel):
    email: EmailStr
    name: str
    lastname: str
    profile_image_url: Optional[HttpUrl] = None

class UserCreate(UserBase):
    password: str  # Solo se usa al crear un usuario

class UserOut(UserBase):
    id: int
    role_id: int
    role: Optional[RoleOut] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True # Permite a Pydantic leer modelos de SQLAlchemy