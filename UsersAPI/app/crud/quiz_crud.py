from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from ..models.quiz_model import Quiz
from ..models.questions_and_answers_model import QuestionsAndAnswers
from ..schemas.quiz_schema import QuizCreate, QuestionCreate


async def create_quiz(db: AsyncSession, quiz: QuizCreate):
    db_quiz = Quiz(
        title=quiz.title or "Untitled Quiz",
        notebook_id=quiz.notebook_id,
        notebook_users_id=quiz.notebook_users_id,
    )
    db.add(db_quiz)
    await db.commit()
    await db.refresh(db_quiz)

    if quiz.questions:
        for question in quiz.questions:
            await create_question(db, question, quiz_id=db_quiz.id)

    # Reload with questions eager-loaded to avoid async lazy-load errors.
    query = select(Quiz).options(joinedload(Quiz.questions)).filter(Quiz.id == db_quiz.id)
    result = await db.execute(query)
    return result.scalars().unique().first()


async def create_question(db: AsyncSession, question: QuestionCreate, quiz_id: Optional[int] = None):
    payload = question.dict()
    if quiz_id is not None:
        payload["quiz_id"] = quiz_id
    db_question = QuestionsAndAnswers(**payload)
    db.add(db_question)
    await db.commit()
    await db.refresh(db_question)
    return db_question


async def get_all_quizzes(db: AsyncSession, skip: int = 0, limit: int = 10):
    query = select(Quiz).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_quiz(db: AsyncSession, quiz_id: int):
    query = (
        select(Quiz)
        .options(joinedload(Quiz.questions))
        .filter(Quiz.id == quiz_id)
    )
    result = await db.execute(query)
    return result.scalars().unique().first()


async def delete_quiz(db: AsyncSession, quiz_id: int):
    db_quiz = await get_quiz(db, quiz_id)
    if db_quiz:
        await db.delete(db_quiz)
        await db.commit()
    return db_quiz


async def get_quizzes_by_notebook(db: AsyncSession, notebook_id: int):
    query = select(Quiz).filter(Quiz.notebook_id == notebook_id)
    result = await db.execute(query)
    return result.scalars().all()


async def get_quizzes_by_user(db: AsyncSession, user_id: int):
    query = select(Quiz).filter(Quiz.notebook_users_id == user_id)
    result = await db.execute(query)
    return result.scalars().all()


async def get_questions_by_quiz(db: AsyncSession, quiz_id: int):
    query = select(QuestionsAndAnswers).filter(QuestionsAndAnswers.quiz_id == quiz_id)
    result = await db.execute(query)
    return result.scalars().all()


async def get_question(db: AsyncSession, question_id: int):
    query = select(QuestionsAndAnswers).filter(QuestionsAndAnswers.id == question_id)
    result = await db.execute(query)
    return result.scalars().first()


async def delete_question(db: AsyncSession, question_id: int):
    db_question = await get_question(db, question_id)
    if db_question:
        await db.delete(db_question)
        await db.commit()
    return db_question
