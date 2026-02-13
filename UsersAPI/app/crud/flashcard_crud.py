from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models.flashcard_model import Flashcard
from ..schemas.flashcard_schema import FlashcardCreate


async def create_flashcard(db: AsyncSession, flashcard: FlashcardCreate):
    db_flashcard = Flashcard(**flashcard.dict())
    db.add(db_flashcard)
    await db.commit()
    await db.refresh(db_flashcard)
    return db_flashcard


async def get_all_flashcards(db: AsyncSession, skip: int = 0, limit: int = 10):
    query = select(Flashcard).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_flashcard(db: AsyncSession, flashcard_id: int):
    query = select(Flashcard).filter(Flashcard.id == flashcard_id)
    result = await db.execute(query)
    return result.scalars().first()


async def delete_flashcard(db: AsyncSession, flashcard_id: int):
    db_flashcard = await get_flashcard(db, flashcard_id)
    if db_flashcard:
        await db.delete(db_flashcard)
        await db.commit()
    return db_flashcard


async def get_flashcards_by_notebook(db: AsyncSession, notebook_id: int):
    query = select(Flashcard).filter(Flashcard.notebook_id == notebook_id)
    result = await db.execute(query)
    return result.scalars().all()


async def get_flashcards_by_user(db: AsyncSession, user_id: int):
    query = select(Flashcard).filter(Flashcard.notebook_users_id == user_id)
    result = await db.execute(query)
    return result.scalars().all()
