from sqlalchemy.orm import Session

from ..models.summary_model import Summary
from ..schemas.summary_schema import SummaryCreate


async def create_summary(db: Session, summary: SummaryCreate):
    db_summary = Summary(**summary.dict())
    db.add(db_summary)
    db.commit()
    db.refresh(db_summary)
    return db_summary


async def get_all_summaries(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Summary).offset(skip).limit(limit).all()


async def get_summary(db: Session, summary_id: int):
    return db.query(Summary).filter(Summary.id == summary_id).first()


async def delete_summary(db: Session, summary_id: int):
    db_summary = await get_summary(db, summary_id)
    if db_summary:
        db.delete(db_summary)
        db.commit()
    return db_summary


async def get_summaries_by_notebook(db: Session, notebook_id: int):
    return db.query(Summary).filter(Summary.notebook_id == notebook_id).all()


async def get_summaries_by_user(db: Session, user_id: int):
    return db.query(Summary).filter(Summary.notebook_users_id == user_id).all()
