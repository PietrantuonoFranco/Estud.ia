from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from ..database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    users = relationship("User", back_populates="role")
