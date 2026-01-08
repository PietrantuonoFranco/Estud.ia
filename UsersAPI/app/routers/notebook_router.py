from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from typing import List
import httpx
import datetime as date

from ..config import conf
from ..database import get_db
from ..schemas.source_schema import SourceOut
from ..schemas.notebook_schema import NotebookOut
from ..security.auth import get_current_user
from ..crud.notebook_crud import (
    create_notebook as create_notebook_crud,
    get_notebook as get_notebook_crud,
    get_all_notebooks,
    delete_notebook as delete_notebook_crud,
    get_all_sources_by_notebook_id,
    get_all_notebooks_by_user_id,
)

# Creamos el router para agrupar estas rutas
router = APIRouter(
    prefix="/notebooks",
    tags=["notebooks"]
)

http_client = httpx.AsyncClient()

@router.on_event("startup")
async def startup_event():
    # El cliente se puede configurar aquí (timeouts, headers, etc.)
    pass

@router.on_event("shutdown")
async def shutdown_event():
    await http_client.aclose()


@router.post("/", response_model=NotebookOut, status_code=status.HTTP_201_CREATED)
async def create_notebook(file: UploadFile, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Método para crear un nuevo notebook."""

    response = await http_client.get(conf.LANGCHAIN_URI + "/create_notebook/", params={"file_name": file})

    notebook_metadata = response.json()
    notebook_metadata.date = date.datetime.now()

    notebook_metadata.users_id = current_user.id

    new_notebook = create_notebook_crud(db=db, notebook=notebook_metadata)

    return new_notebook

@router.get("/", response_model=List[NotebookOut], status_code=status.HTTP_200_OK)
async def read_notebooks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Método para obtener todos los notebooks con paginación."""
    return get_all_notebooks(db, skip=skip, limit=limit)


@router.get("/{notebook_id}", response_model=NotebookOut, status_code=status.HTTP_200_OK)
async def read_notebook(notebook_id: int, db: Session = Depends(get_db)):
    """Método para obtener un notebook por su ID."""
    notebook = get_notebook_crud(db, notebook_id=notebook_id)

    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook no encontrado")
    
    return notebook


@router.delete("/{notebook_id}", response_model=NotebookOut, status_code=status.HTTP_200_OK)
async def delete_notebook(notebook_id: int, db: Session = Depends(get_db)):
    """Método para eliminar un notebook por su ID."""
    notebook = get_notebook_crud(db, notebook_id=notebook_id)

    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook no encontrado")
    
    return delete_notebook_crud(db, notebook_id=notebook_id)

@router.get("/{notebook_id}/sources", response_model=List[SourceOut], status_code=status.HTTP_200_OK)
async def read_sources_by_notebook_id(notebook_id: int, db: Session = Depends(get_db)):
    """Método para obtener las fuentes (sources) asociadas a un notebook específico."""
    notebook = get_notebook_crud(db, notebook_id=notebook_id)
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook no encontrado")

    sources = get_all_sources_by_notebook_id(db, notebook_id=notebook_id)

    if not sources:
        raise HTTPException(status_code=404, detail="Fuentes no encontradas para este notebook")
    
    return sources

@router.get("/user/{user_id}", response_model=List[NotebookOut], status_code=status.HTTP_200_OK)
async def read_notebooks_by_user_id(user_id: int, db: Session = Depends(get_db)):
    """Método para obtener los notebooks asociados a un usuario específico."""
    notebooks = get_all_notebooks_by_user_id(db, user_id=user_id)

    if not notebooks:
        raise HTTPException(status_code=404, detail="No se encontraron notebooks para este usuario")
    
    return notebooks