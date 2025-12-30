from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.flashcard_schema import FlashcardCreate, FlashcardOut
from ..crud.flashcard_crud import (
    create_flashcard,
    get_all_flashcards,
    get_flashcard,
    delete_flashcard,
    get_flashcards_by_notebook,
    get_flashcards_by_user,
)

router = APIRouter(prefix="/flashcards", tags=["flashcards"])


@router.post("/", response_model=FlashcardOut, status_code=status.HTTP_201_CREATED)
def create_flashcard_endpoint(flashcard: FlashcardCreate, db: Session = Depends(get_db)):
    return create_flashcard(db=db, flashcard=flashcard)


@router.get("/", response_model=List[FlashcardOut], status_code=status.HTTP_200_OK)
def read_flashcards(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_flashcards(db, skip=skip, limit=limit)


@router.get("/{flashcard_id}", response_model=FlashcardOut, status_code=status.HTTP_200_OK)
def read_flashcard(flashcard_id: int, db: Session = Depends(get_db)):
    flashcard = get_flashcard(db, flashcard_id=flashcard_id)
    if not flashcard:
        raise HTTPException(status_code=404, detail="Flashcard no encontrada")
    return flashcard


@router.delete("/{flashcard_id}", response_model=FlashcardOut, status_code=status.HTTP_200_OK)
def delete_flashcard_endpoint(flashcard_id: int, db: Session = Depends(get_db)):
    flashcard = get_flashcard(db, flashcard_id=flashcard_id)
    if not flashcard:
        raise HTTPException(status_code=404, detail="Flashcard no encontrada")
    return delete_flashcard(db, flashcard_id=flashcard_id)


@router.get("/notebook/{notebook_id}", response_model=List[FlashcardOut], status_code=status.HTTP_200_OK)
def read_flashcards_by_notebook(notebook_id: int, db: Session = Depends(get_db)):
    flashcards = get_flashcards_by_notebook(db, notebook_id=notebook_id)
    if not flashcards:
        raise HTTPException(status_code=404, detail="No se encontraron flashcards para este notebook")
    return flashcards


@router.get("/user/{user_id}", response_model=List[FlashcardOut], status_code=status.HTTP_200_OK)
def read_flashcards_by_user(user_id: int, db: Session = Depends(get_db)):
    flashcards = get_flashcards_by_user(db, user_id=user_id)
    if not flashcards:
        raise HTTPException(status_code=404, detail="No se encontraron flashcards para este usuario")
    return flashcards
