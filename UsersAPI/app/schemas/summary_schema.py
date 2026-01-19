from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SummaryBase(BaseModel):
    text: str
    notebook_id: int
    notebook_users_id: int


class SummaryCreate(SummaryBase):
    pass


class SummaryOut(SummaryBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
