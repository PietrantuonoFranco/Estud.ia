from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..database import get_db
from ..schemas.flashcard_schema import FlashcardCreate, FlashcardOut
from ..security.auth import get_current_user
from ..utils.validate_admin import validate_admin
from ..crud.flashcard_crud import (
    create_flashcard,
    get_all_flashcards,
    get_flashcard,
    delete_flashcard,
    get_flashcards_by_notebook,
    get_flashcards_by_user,
)
from ..crud.notebook_crud import get_notebook

router = APIRouter(prefix="/flashcards", tags=["flashcards"])


@router.post("/", response_model=FlashcardOut, status_code=status.HTTP_201_CREATED)
async def create_flashcard_endpoint(
    flashcard: FlashcardCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    notebook = await get_notebook(db, notebook_id=flashcard.notebook_id)
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook no encontrado")

    if not validate_admin(current_user) and notebook.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para crear esta flashcard")

    if not validate_admin(current_user) and flashcard.notebook_users_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para crear esta flashcard")

    return await create_flashcard(db=db, flashcard=flashcard)


@router.get("/", response_model=List[FlashcardOut], status_code=status.HTTP_200_OK)
async def read_flashcards(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await get_all_flashcards(db, skip=skip, limit=limit)


@router.get("/{flashcard_id}", response_model=FlashcardOut, status_code=status.HTTP_200_OK)
async def read_flashcard(flashcard_id: int, db: AsyncSession = Depends(get_db)):
    flashcard = await get_flashcard(db, flashcard_id=flashcard_id)
    if not flashcard:
        raise HTTPException(status_code=404, detail="Flashcard no encontrada")
    return flashcard


@router.delete("/{flashcard_id}", response_model=FlashcardOut, status_code=status.HTTP_200_OK)
async def delete_flashcard_endpoint(
    flashcard_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    flashcard = await get_flashcard(db, flashcard_id=flashcard_id)
    if not flashcard:
        raise HTTPException(status_code=404, detail="Flashcard no encontrada")

    if not validate_admin(current_user) and flashcard.notebook_users_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar esta flashcard")

    return await delete_flashcard(db, flashcard_id=flashcard_id)


@router.get("/notebook/{notebook_id}", response_model=List[FlashcardOut], status_code=status.HTTP_200_OK)
async def read_flashcards_by_notebook(notebook_id: int, db: AsyncSession = Depends(get_db)):
    flashcards = await get_flashcards_by_notebook(db, notebook_id=notebook_id)
    if not flashcards:
        raise HTTPException(status_code=404, detail="No se encontraron flashcards para este notebook")
    return flashcards


@router.get("/user/{user_id}", response_model=List[FlashcardOut], status_code=status.HTTP_200_OK)
async def read_flashcards_by_user(user_id: int, db: AsyncSession = Depends(get_db)):
    flashcards = await get_flashcards_by_user(db, user_id=user_id)
    if not flashcards:
        raise HTTPException(status_code=404, detail="No se encontraron flashcards para este usuario")
    return flashcards
