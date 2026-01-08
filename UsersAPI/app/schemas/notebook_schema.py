from pydantic import BaseModel, Field
from datetime import datetime

# --- SCHEMAS DE NOTEBOOK ---

class NotebookBase(BaseModel):
    title: str
    icon: str
    date: datetime = Field(default_factory=datetime.now)

class NotebookCreate(NotebookBase):
    users_id: int

class NotebookOut(NotebookBase):
    id: int
    users_id: int

    class Config:
        from_attributes = True