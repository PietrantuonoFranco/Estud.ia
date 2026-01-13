from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from ..database import Base

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    
    # Claves foráneas
    notebook_id = Column(Integer, ForeignKey("notebooks.id"), nullable=True)

    # Relación
    notebook = relationship("Notebook", back_populates="sources")