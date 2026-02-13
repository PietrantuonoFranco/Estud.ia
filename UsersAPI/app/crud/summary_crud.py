from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models.summary_model import Summary
from ..schemas.summary_schema import SummaryCreate


async def create_summary(db: AsyncSession, summary: SummaryCreate):
    db_summary = Summary(**summary.dict())
    db.add(db_summary)
    await db.commit()
    await db.refresh(db_summary)
    return db_summary


async def get_all_summaries(db: AsyncSession, skip: int = 0, limit: int = 10):
    query = select(Summary).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_summary(db: AsyncSession, summary_id: int):
    query = select(Summary).filter(Summary.id == summary_id)
    result = await db.execute(query)
    return result.scalars().first()


async def delete_summary(db: AsyncSession, summary_id: int):
    db_summary = await get_summary(db, summary_id)
    if db_summary:
        await db.delete(db_summary)
        await db.commit()
    return db_summary


async def get_summaries_by_notebook(db: AsyncSession, notebook_id: int):
    query = select(Summary).filter(Summary.notebook_id == notebook_id)
    result = await db.execute(query)
    return result.scalars().all()


async def get_summaries_by_user(db: AsyncSession, user_id: int):
    query = select(Summary).filter(Summary.notebook_users_id == user_id)
    result = await db.execute(query)
    return result.scalars().all()
