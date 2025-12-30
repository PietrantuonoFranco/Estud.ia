from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Flashcard(Base):
    __tablename__ = "flashcards"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(255), nullable=False)
    answer = Column(String(255), nullable=False)
    notebook_id = Column(Integer, ForeignKey("notebook.id"), nullable=False)
    notebook_users_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    notebook = relationship("Notebook", back_populates="flashcards")
    user = relationship("User")
