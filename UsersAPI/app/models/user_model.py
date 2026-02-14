from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(45), unique=True, nullable=False)
    name = Column(String(45), nullable=False)
    lastname = Column(String(45), nullable=False)
    password = Column(String(255), nullable=False)
    profile_image_url = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    # Relación: Un usuario puede tener varios notebooks
    notebooks = relationship("Notebook", back_populates="owner")
    role = relationship("Role", back_populates="users")