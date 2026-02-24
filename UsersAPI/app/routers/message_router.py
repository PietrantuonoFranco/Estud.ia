from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import httpx
from pydantic import BaseModel

from ..config import conf
from ..database import get_db
from ..schemas.message_schema import MessageCreate, MessageOut
from ..security.auth import get_current_user
from ..utils.validate_admin import validate_admin
from ..crud.notebook_crud import get_notebook
from ..crud.message_crud import (
    create_message,
    get_all_messages,
    get_message,
    delete_message,
    get_messages_by_notebook,
    get_messages_by_user,
)

class MessageRequest(BaseModel):
    text: str
    notebook_id: int

router = APIRouter(prefix="/messages", tags=["messages"])
http_client = httpx.AsyncClient()

@router.on_event("startup")
async def startup_event():
    pass

@router.on_event("shutdown")
async def shutdown_event():
    await http_client.aclose()


@router.post("/", response_model=MessageOut, status_code=status.HTTP_201_CREATED)
async def create_message_endpoint(message: MessageCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    """Método para crear un nuevo mensaje."""
    notebook = await get_notebook(db, notebook_id=message.notebook_id)
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")

    if not validate_admin(current_user) and notebook.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para crear este mensaje")

    if not validate_admin(current_user) and message.notebook_users_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para crear este mensaje")

    return await create_message(db=db, message=message)

@router.post("/user", response_model=MessageOut, status_code=status.HTTP_201_CREATED)
async def create_user_message(message: MessageRequest, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    """Método para crear un mensaje enviado por el usuario."""
    notebook = await get_notebook(db, notebook_id=message.notebook_id)
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")

    if not validate_admin(current_user) and notebook.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para crear este mensaje")

    message_data = message.dict()
    message_data['is_user_message'] = True
    message_data['text'] = message.text
    message_data['notebook_id'] = message.notebook_id
    message_data['notebook_users_id'] = current_user.id

    message = MessageCreate(**message_data)
    return await create_message(db=db, message=message)

@router.post("/llm", response_model=MessageOut, status_code=status.HTTP_201_CREATED)
async def create_llm_message(message: MessageRequest
, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    """Método para crear un mensaje generado por el LLM basado en la entrada del usuario."""
    message_data = message.dict()
    message_data['is_user_message'] = False
    message_data['text'] = message.text

    notebook = await get_notebook(db, notebook_id=message.notebook_id)
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")

    if not validate_admin(current_user) and notebook.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para crear este mensaje")
    
    message_data['notebook_id'] = message.notebook_id
    message_data['notebook_users_id'] = current_user.id
    
    # Obtener historial de mensajes del notebook
    chat_history = await get_messages_by_notebook(db, notebook_id=message.notebook_id)
    
    # Convertir mensajes a dict serializable (evitar atributos internos de SQLAlchemy)
    chat_history_dicts = []
    if chat_history:
        for msg in chat_history:
            chat_history_dicts.append({
                "id": msg.id,
                "text": msg.text,
                "notebook_id": msg.notebook_id,
                "notebook_users_id": msg.notebook_users_id,
                "is_user_message": msg.is_user_message,
                "created_at": msg.created_at.isoformat() if msg.created_at else None,
                "updated_at": msg.updated_at.isoformat() if msg.updated_at else None,
            })
    
    try:
        response = await http_client.post(
            f"{conf.LANGCHAIN_URI}/chat/rag",
            json={
                "question": message.text,
                "pdf_ids": [source.id for source in notebook.sources],
                "chatHistory": chat_history_dicts,
            },
            headers={"X-API-Key": conf.LANGCHAIN_API_KEY},
            timeout=60.0
        )

        response.raise_for_status()

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Error en servicio externo de Langchain")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {str(e)}")

    message_response_data = response.json()
    message_data['text'] = message_response_data.get('generation', '')

    message = MessageCreate(**message_data)
    
    return await create_message(db=db, message=message)


@router.get("/", response_model=List[MessageOut], status_code=status.HTTP_200_OK)
async def read_messages(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    """Método para obtener todos los mensajes con paginación."""
    return await get_all_messages(db, skip=skip, limit=limit)


@router.get("/{message_id}", response_model=MessageOut, status_code=status.HTTP_200_OK)
async def read_message(message_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    """Método para obtener un mensaje por su ID."""
    message = await get_message(db, message_id=message_id)
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    return message


@router.delete("/{message_id}", response_model=MessageOut, status_code=status.HTTP_200_OK)
async def delete_message_endpoint(message_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    """Método para eliminar un mensaje por su ID."""
    message = await get_message(db, message_id=message_id)
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    if not validate_admin(current_user) and message.notebook_users_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar este mensaje")
    
    return await delete_message(db, message_id=message_id)


@router.get("/notebook/{notebook_id}", response_model=List[MessageOut], status_code=status.HTTP_200_OK)
async def read_messages_by_notebook(notebook_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    """Método para obtener todos los mensajes de un notebook específico."""
    messages = await get_messages_by_notebook(db, notebook_id=notebook_id)
    
    if not messages:
        raise HTTPException(status_code=404, detail="Notebook messages not found")
    
    return messages


@router.get("/user/", response_model=List[MessageOut], status_code=status.HTTP_200_OK)
async def read_messages_by_user(user_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    """Método para obtener todos los mensajes de un usuario específico."""
    messages = await get_messages_by_user(db, user_id=current_user.id)
    
    if not messages:
        raise HTTPException(status_code=404, detail="User messages not found")
    
    return messages
