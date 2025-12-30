from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import Base


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255), nullable=False)
    notebook_id = Column(Integer, ForeignKey("notebook.id"), nullable=False)
    notebook_users_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_user_message = Column(Boolean, default=True, nullable=False)

    notebook = relationship("Notebook", back_populates="messages")
    user = relationship("User")
