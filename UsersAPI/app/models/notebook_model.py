from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Notebook(Base):
    __tablename__ = "notebook"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(45), nullable=False)
    icon = Column(String(45))
    date = Column(Date)
    
    # Clave foránea
    users_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relaciones
    owner = relationship("User", back_populates="notebooks")
    sources = relationship("Source", back_populates="notebook")
    messages = relationship("Message", back_populates="notebook")
    summaries = relationship("Summary", back_populates="notebook")
    flashcards = relationship("Flashcard", back_populates="notebook")
    quizzes = relationship("Quiz", back_populates="notebook")