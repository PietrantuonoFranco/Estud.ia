from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, func, String
from sqlalchemy.orm import relationship
from ..database import Base


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    text = Column(Text, nullable=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    notebook_id = Column(Integer, ForeignKey("notebooks.id"), nullable=False)
    notebook_users_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    notebook = relationship("Notebook", back_populates="summaries")
    user = relationship("User")
