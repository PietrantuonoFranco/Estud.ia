from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

from .message_schema import MessageOut

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
    messages: List[MessageOut] = []

    class Config:
        from_attributes = True