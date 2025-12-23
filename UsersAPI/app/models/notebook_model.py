from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Notebook(Base):
    __tablename__ = "notebook"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(45), nullable=False)
    icon = Column(String(45))
    date = Column(Date)
    collection_name = Column(String(45))
    
    # Clave foránea
    users_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relaciones
    owner = relationship("User", back_populates="notebooks")
    sources = relationship("Source", back_populates="notebook")