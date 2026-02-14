from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleOut(RoleBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
