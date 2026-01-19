from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MessageBase(BaseModel):
    text: str
    notebook_id: int
    notebook_users_id: int
    is_user_message: bool = True


class MessageCreate(MessageBase):
    pass


class MessageOut(MessageBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
