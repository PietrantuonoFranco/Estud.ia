from pydantic import BaseModel

# --- SCHEMAS DE SOURCE ---

class SourceBase(BaseModel):
    notebook_id: int

class SourceOut(SourceBase):
    id: int
    # No incluimos pdf_file en la salida por defecto porque es pesado (binario)
    
    class Config:
        from_attributes = True