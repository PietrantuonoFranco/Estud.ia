from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.quiz_schema import QuizCreate, QuizOut, QuestionCreate, QuestionOut
from ..crud.quiz_crud import (
    create_quiz,
    get_all_quizzes,
    get_quiz,
    delete_quiz,
    get_quizzes_by_notebook,
    get_quizzes_by_user,
    get_questions_by_quiz,
    create_question,
    get_question,
    delete_question,
)

router = APIRouter(prefix="/quizzes", tags=["quizzes"])


@router.post("/", response_model=QuizOut, status_code=status.HTTP_201_CREATED)
async def create_quiz_endpoint(quiz: QuizCreate, db: Session = Depends(get_db)):
    return await create_quiz(db=db, quiz=quiz)


@router.get("/", response_model=List[QuizOut], status_code=status.HTTP_200_OK)
async def read_quizzes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return await get_all_quizzes(db, skip=skip, limit=limit)


@router.get("/{quiz_id}", response_model=QuizOut, status_code=status.HTTP_200_OK)
async def read_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = await get_quiz(db, quiz_id=quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz no encontrado")
    return quiz


@router.delete("/{quiz_id}", response_model=QuizOut, status_code=status.HTTP_200_OK)
async def delete_quiz_endpoint(quiz_id: int, db: Session = Depends(get_db)):
    quiz = await get_quiz(db, quiz_id=quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz no encontrado")
    return await delete_quiz(db, quiz_id=quiz_id)


@router.get("/notebook/{notebook_id}", response_model=List[QuizOut], status_code=status.HTTP_200_OK)
async def read_quizzes_by_notebook(notebook_id: int, db: Session = Depends(get_db)):
    quizzes = await get_quizzes_by_notebook(db, notebook_id=notebook_id)
    if not quizzes:
        raise HTTPException(status_code=404, detail="No se encontraron quizzes para este notebook")
    return quizzes


@router.get("/user/{user_id}", response_model=List[QuizOut], status_code=status.HTTP_200_OK)
async def read_quizzes_by_user(user_id: int, db: Session = Depends(get_db)):
    quizzes = await get_quizzes_by_user(db, user_id=user_id)
    if not quizzes:
        raise HTTPException(status_code=404, detail="No se encontraron quizzes para este usuario")
    return quizzes


@router.post("/{quiz_id}/questions", response_model=QuestionOut, status_code=status.HTTP_201_CREATED)
async def create_question_endpoint(quiz_id: int, question: QuestionCreate, db: Session = Depends(get_db)):
    if not await get_quiz(db, quiz_id=quiz_id):
        raise HTTPException(status_code=404, detail="Quiz no encontrado")
    return await create_question(db, question, quiz_id=quiz_id)


@router.get("/{quiz_id}/questions", response_model=List[QuestionOut], status_code=status.HTTP_200_OK)
async def read_questions_by_quiz(quiz_id: int, db: Session = Depends(get_db)):
    if not await get_quiz(db, quiz_id=quiz_id):
        raise HTTPException(status_code=404, detail="Quiz no encontrado")
    questions = await get_questions_by_quiz(db, quiz_id=quiz_id)
    if not questions:
        raise HTTPException(status_code=404, detail="No se encontraron preguntas para este quiz")
    return questions


@router.delete("/questions/{question_id}", response_model=QuestionOut, status_code=status.HTTP_200_OK)
async def delete_question_endpoint(question_id: int, db: Session = Depends(get_db)):
    question = await get_question(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    return await delete_question(db, question_id=question_id)
