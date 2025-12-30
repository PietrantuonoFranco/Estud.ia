from pydantic import BaseModel
from typing import Optional
from datetime import date

# --- SCHEMAS DE NOTEBOOK ---

class NotebookBase(BaseModel):
    title: str
    icon: Optional[str] = None
    date: Optional[date] = None

class NotebookCreate(NotebookBase):
    users_id: int

class NotebookOut(NotebookBase):
    id: int
    users_id: int

    class Config:
        from_attributes = True