from typing import Optional
from sqlalchemy.orm import Session

from ..models.quiz_model import Quiz
from ..models.questions_and_answers_model import QuestionsAndAnswers
from ..schemas.quiz_schema import QuizCreate, QuestionCreate


def create_quiz(db: Session, quiz: QuizCreate):
    db_quiz = Quiz(
        notebook_id=quiz.notebook_id,
        notebook_users_id=quiz.notebook_users_id,
    )
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)

    if quiz.questions:
        for question in quiz.questions:
            create_question(db, question, quiz_id=db_quiz.id)

    db.refresh(db_quiz)
    return db_quiz


def create_question(db: Session, question: QuestionCreate, quiz_id: Optional[int] = None):
    payload = question.dict()
    if quiz_id is not None:
        payload["quiz_id"] = quiz_id
    db_question = QuestionsAndAnswers(**payload)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def get_all_quizzes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Quiz).offset(skip).limit(limit).all()


def get_quiz(db: Session, quiz_id: int):
    return db.query(Quiz).filter(Quiz.id == quiz_id).first()


def delete_quiz(db: Session, quiz_id: int):
    db_quiz = get_quiz(db, quiz_id)
    if db_quiz:
        db.delete(db_quiz)
        db.commit()
    return db_quiz


def get_quizzes_by_notebook(db: Session, notebook_id: int):
    return db.query(Quiz).filter(Quiz.notebook_id == notebook_id).all()


def get_quizzes_by_user(db: Session, user_id: int):
    return db.query(Quiz).filter(Quiz.notebook_users_id == user_id).all()


def get_questions_by_quiz(db: Session, quiz_id: int):
    return db.query(QuestionsAndAnswers).filter(QuestionsAndAnswers.quiz_id == quiz_id).all()


def get_question(db: Session, question_id: int):
    return db.query(QuestionsAndAnswers).filter(QuestionsAndAnswers.id == question_id).first()


def delete_question(db: Session, question_id: int):
    db_question = get_question(db, question_id)
    if db_question:
        db.delete(db_question)
        db.commit()
    return db_question
