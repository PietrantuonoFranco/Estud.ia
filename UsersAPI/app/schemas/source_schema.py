from pydantic import BaseModel
from typing import Optional
# --- SCHEMAS DE SOURCE ---

class SourceBase(BaseModel):
    name: str
    notebook_id: int | None = None
    
class SourceCreate(SourceBase):
    pass

class SourceOut(SourceBase):
    id: int
    
    class Config:
        from_attributes = True