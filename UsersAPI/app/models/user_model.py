from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base

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