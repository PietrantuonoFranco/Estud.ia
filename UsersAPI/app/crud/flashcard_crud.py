from sqlalchemy.orm import Session

from ..models.flashcard_model import Flashcard
from ..schemas.flashcard_schema import FlashcardCreate


async def create_flashcard(db: Session, flashcard: FlashcardCreate):
    db_flashcard = Flashcard(**flashcard.dict())
    db.add(db_flashcard)
    db.commit()
    db.refresh(db_flashcard)
    return db_flashcard


async def get_all_flashcards(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Flashcard).offset(skip).limit(limit).all()


async def get_flashcard(db: Session, flashcard_id: int):
    return db.query(Flashcard).filter(Flashcard.id == flashcard_id).first()


async def delete_flashcard(db: Session, flashcard_id: int):
    db_flashcard = await get_flashcard(db, flashcard_id)
    if db_flashcard:
        db.delete(db_flashcard)
        db.commit()
    return db_flashcard


async def get_flashcards_by_notebook(db: Session, notebook_id: int):
    return db.query(Flashcard).filter(Flashcard.notebook_id == notebook_id).all()


async def get_flashcards_by_user(db: Session, user_id: int):
    return db.query(Flashcard).filter(Flashcard.notebook_users_id == user_id).all()
