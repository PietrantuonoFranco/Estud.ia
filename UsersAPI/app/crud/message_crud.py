from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models.message_model import Message
from ..schemas.message_schema import MessageCreate


async def create_message(db: AsyncSession, message: MessageCreate):
    db_message = Message(**message.dict())
    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)
    return db_message


async def get_all_messages(db: AsyncSession, skip: int = 0, limit: int = 10):
    query = select(Message).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_message(db: AsyncSession, message_id: int):
    query = select(Message).filter(Message.id == message_id)
    result = await db.execute(query)
    return result.scalars().first()


async def delete_message(db: AsyncSession, message_id: int):
    db_message = await get_message(db, message_id)
    if db_message:
        await db.delete(db_message)
        await db.commit()
    return db_message


async def get_messages_by_notebook(db: AsyncSession, notebook_id: int):
    query = select(Message).filter(Message.notebook_id == notebook_id)
    result = await db.execute(query)
    return result.scalars().all()


async def get_messages_by_user(db: AsyncSession, user_id: int):
    query = select(Message).filter(Message.notebook_users_id == user_id)
    result = await db.execute(query)
    return result.scalars().all()
