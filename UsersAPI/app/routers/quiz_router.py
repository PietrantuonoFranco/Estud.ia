from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..database import get_db
from ..schemas.quiz_schema import QuizCreate, QuizOut, QuestionCreate, QuestionOut
from ..security.auth import get_current_user
from ..utils.validate_admin import validate_admin
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
from ..crud.notebook_crud import get_notebook

router = APIRouter(prefix="/quizzes", tags=["quizzes"])


@router.post("/", response_model=QuizOut, status_code=status.HTTP_201_CREATED)
async def create_quiz_endpoint(
    quiz: QuizCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    notebook = await get_notebook(db, notebook_id=quiz.notebook_id)
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook no encontrado")

    if not validate_admin(current_user) and notebook.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para crear este quiz")

    if not validate_admin(current_user) and quiz.notebook_users_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para crear este quiz")

    return await create_quiz(db=db, quiz=quiz)


@router.get("/", response_model=List[QuizOut], status_code=status.HTTP_200_OK)
async def read_quizzes(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await get_all_quizzes(db, skip=skip, limit=limit)


@router.get("/{quiz_id}", response_model=QuizOut, status_code=status.HTTP_200_OK)
async def read_quiz(quiz_id: int, db: AsyncSession = Depends(get_db)):
    quiz = await get_quiz(db, quiz_id=quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz no encontrado")
    return quiz


@router.delete("/{quiz_id}", response_model=QuizOut, status_code=status.HTTP_200_OK)
async def delete_quiz_endpoint(
    quiz_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    quiz = await get_quiz(db, quiz_id=quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz no encontrado")

    if not validate_admin(current_user) and quiz.notebook_users_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar este quiz")

    return await delete_quiz(db, quiz_id=quiz_id)


@router.get("/notebook/{notebook_id}", response_model=List[QuizOut], status_code=status.HTTP_200_OK)
async def read_quizzes_by_notebook(notebook_id: int, db: AsyncSession = Depends(get_db)):
    quizzes = await get_quizzes_by_notebook(db, notebook_id=notebook_id)
    if not quizzes:
        raise HTTPException(status_code=404, detail="No se encontraron quizzes para este notebook")
    return quizzes


@router.get("/user/{user_id}", response_model=List[QuizOut], status_code=status.HTTP_200_OK)
async def read_quizzes_by_user(user_id: int, db: AsyncSession = Depends(get_db)):
    quizzes = await get_quizzes_by_user(db, user_id=user_id)
    if not quizzes:
        raise HTTPException(status_code=404, detail="No se encontraron quizzes para este usuario")
    return quizzes


@router.post("/{quiz_id}/questions", response_model=QuestionOut, status_code=status.HTTP_201_CREATED)
async def create_question_endpoint(
    quiz_id: int,
    question: QuestionCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    quiz = await get_quiz(db, quiz_id=quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz no encontrado")

    if not validate_admin(current_user) and quiz.notebook_users_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para agregar preguntas a este quiz")

    return await create_question(db, question, quiz_id=quiz_id)


@router.get("/{quiz_id}/questions", response_model=List[QuestionOut], status_code=status.HTTP_200_OK)
async def read_questions_by_quiz(quiz_id: int, db: AsyncSession = Depends(get_db)):
    if not await get_quiz(db, quiz_id=quiz_id):
        raise HTTPException(status_code=404, detail="Quiz no encontrado")
    questions = await get_questions_by_quiz(db, quiz_id=quiz_id)
    if not questions:
        raise HTTPException(status_code=404, detail="No se encontraron preguntas para este quiz")
    return questions


@router.delete("/questions/{question_id}", response_model=QuestionOut, status_code=status.HTTP_200_OK)
async def delete_question_endpoint(
    question_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    question = await get_question(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")

    quiz = await get_quiz(db, quiz_id=question.quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz no encontrado")

    if not validate_admin(current_user) and quiz.notebook_users_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar esta pregunta")

    return await delete_question(db, question_id=question_id)
