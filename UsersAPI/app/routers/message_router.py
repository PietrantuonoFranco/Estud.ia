from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.message_schema import MessageCreate, MessageOut
from ..crud.message_crud import (
    create_message,
    get_all_messages,
    get_message,
    delete_message,
    get_messages_by_notebook,
    get_messages_by_user,
)

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/", response_model=MessageOut, status_code=status.HTTP_201_CREATED)
def create_message_endpoint(message: MessageCreate, db: Session = Depends(get_db)):
    return create_message(db=db, message=message)


@router.get("/", response_model=List[MessageOut], status_code=status.HTTP_200_OK)
def read_messages(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_messages(db, skip=skip, limit=limit)


@router.get("/{message_id}", response_model=MessageOut, status_code=status.HTTP_200_OK)
def read_message(message_id: int, db: Session = Depends(get_db)):
    message = get_message(db, message_id=message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    return message


@router.delete("/{message_id}", response_model=MessageOut, status_code=status.HTTP_200_OK)
def delete_message_endpoint(message_id: int, db: Session = Depends(get_db)):
    message = get_message(db, message_id=message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    return delete_message(db, message_id=message_id)


@router.get("/notebook/{notebook_id}", response_model=List[MessageOut], status_code=status.HTTP_200_OK)
def read_messages_by_notebook(notebook_id: int, db: Session = Depends(get_db)):
    messages = get_messages_by_notebook(db, notebook_id=notebook_id)
    if not messages:
        raise HTTPException(status_code=404, detail="No se encontraron mensajes para este notebook")
    return messages


@router.get("/user/{user_id}", response_model=List[MessageOut], status_code=status.HTTP_200_OK)
def read_messages_by_user(user_id: int, db: Session = Depends(get_db)):
    messages = get_messages_by_user(db, user_id=user_id)
    if not messages:
        raise HTTPException(status_code=404, detail="No se encontraron mensajes para este usuario")
    return messages
