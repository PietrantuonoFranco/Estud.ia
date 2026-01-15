from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..database import Base


class Flashcard(Base):
    __tablename__ = "flashcards"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(255), nullable=False)
    answer = Column(Text, nullable=False)
    notebook_id = Column(Integer, ForeignKey("notebooks.id"), nullable=False)
    notebook_users_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    notebook = relationship("Notebook", back_populates="flashcards")
    user = relationship("User")
