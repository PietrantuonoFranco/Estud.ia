from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class QuestionsAndAnswers(Base):
    __tablename__ = "questions_and_answers"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(255), nullable=False)
    answer = Column(String(255), nullable=False)
    incorrect_answer_1 = Column(String(255), nullable=False)
    incorrect_answer_2 = Column(String(255), nullable=False)
    incorrect_answer_3 = Column(String(255), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)

    quiz = relationship("Quiz", back_populates="questions")
