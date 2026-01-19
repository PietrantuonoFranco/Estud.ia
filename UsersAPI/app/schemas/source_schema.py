from pydantic import BaseModel
from typing import Optional
from datetime import datetime
# --- SCHEMAS DE SOURCE ---

class SourceBase(BaseModel):
    name: str
    notebook_id: int | None = None
    
class SourceCreate(SourceBase):
    pass

class SourceOut(SourceBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True