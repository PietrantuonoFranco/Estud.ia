from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Quiz(Base):
    __tablename__ = "quiz"

    id = Column(Integer, primary_key=True, index=True)
    notebook_id = Column(Integer, ForeignKey("notebook.id"), nullable=False)
    notebook_users_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    notebook = relationship("Notebook", back_populates="quizzes")
    user = relationship("User")
    questions = relationship("QuestionsAndAnswers", back_populates="quiz")
