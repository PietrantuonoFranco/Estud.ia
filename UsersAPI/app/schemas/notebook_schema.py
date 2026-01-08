from pydantic import BaseModel, Field
from datetime import datetime

# --- SCHEMAS DE NOTEBOOK ---

class NotebookBase(BaseModel):
    title: str
    icon: str
    description: str
    date: datetime = Field(default_factory=datetime.now)

class NotebookCreate(NotebookBase):
    user_id: int

class NotebookOut(NotebookBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True