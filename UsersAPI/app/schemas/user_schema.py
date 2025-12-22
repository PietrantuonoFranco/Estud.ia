from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional

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

    class Config:
        from_attributes = True # Permite a Pydantic leer modelos de SQLAlchemy