from sqlalchemy import Column, Integer, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from ..database import Base

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    pdf_file = Column(LargeBinary) # Para el tipo BLOB del diagrama
    
    # Claves foráneas
    notebook_id = Column(Integer, ForeignKey("notebooks.id"), nullable=False)

    # Relación
    notebook = relationship("Notebook", back_populates="sources")