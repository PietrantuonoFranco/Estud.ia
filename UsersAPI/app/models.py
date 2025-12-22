from sqlalchemy import Column, Integer, String, Date, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(45), unique=True, nullable=False)
    name = Column(String(45), nullable=False)
    lastname = Column(String(45), nullable=False)
    password = Column(String(45), nullable=False)
    profile_image_url = Column(String(255))

    # Relación: Un usuario puede tener varios notebooks
    notebooks = relationship("Notebook", back_populates="owner")


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


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    pdf_file = Column(LargeBinary) # Para el tipo BLOB del diagrama
    
    # Claves foráneas
    notebook_id = Column(Integer, ForeignKey("notebook.id"), nullable=False)

    # Relación
    notebook = relationship("Notebook", back_populates="sources")