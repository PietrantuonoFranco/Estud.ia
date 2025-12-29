from pydantic import BaseModel

# --- SCHEMAS DE SOURCE ---

class SourceBase(BaseModel):
    notebook_id: int

class SourceCreate(SourceBase):
    # Contenido binario del PDF a almacenar
    pdf_file: bytes

class SourceOut(SourceBase):
    id: int
    # No incluimos pdf_file en la salida por defecto porque es pesado (binario)
    
    class Config:
        from_attributes = True