from sqlalchemy.orm import Session

from ..models.message_model import Message
from ..schemas.message_schema import MessageCreate


def create_message(db: Session, message: MessageCreate):
    db_message = Message(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    # Asegurar que el objeto tenga todos los atributos antes de retornar
    db.expunge(db_message)
    return db_message


def get_all_messages(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Message).offset(skip).limit(limit).all()


def get_message(db: Session, message_id: int):
    return db.query(Message).filter(Message.id == message_id).first()


def delete_message(db: Session, message_id: int):
    db_message = get_message(db, message_id)
    if db_message:
        db.delete(db_message)
        db.commit()
    return db_message


def get_messages_by_notebook(db: Session, notebook_id: int):
    return db.query(Message).filter(Message.notebook_id == notebook_id).all()


def get_messages_by_user(db: Session, user_id: int):
    return db.query(Message).filter(Message.notebook_users_id == user_id).all()
