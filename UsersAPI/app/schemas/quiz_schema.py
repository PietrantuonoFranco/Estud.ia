from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class QuestionBase(BaseModel):
    question: str
    answer: str
    incorrect_answer_1: str
    incorrect_answer_2: str
    incorrect_answer_3: str
    quiz_id: Optional[int] = None


class QuestionCreate(QuestionBase):
    pass


class QuestionOut(QuestionBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class QuizBase(BaseModel):
    notebook_id: int
    notebook_users_id: int


class QuizCreate(QuizBase):
    title: Optional[str] = None
    questions: Optional[List[QuestionCreate]] = None


class QuizOut(QuizBase):
    id: int
    title: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class QuizWithQuestions(QuizOut):
    questions_and_answers: List[QuestionOut] = Field(default_factory=list)
