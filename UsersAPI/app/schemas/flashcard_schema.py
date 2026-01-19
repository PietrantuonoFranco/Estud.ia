from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FlashcardBase(BaseModel):
    question: str
    answer: str
    notebook_id: int
    notebook_users_id: int


class FlashcardCreate(FlashcardBase):
    pass


class FlashcardOut(FlashcardBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
