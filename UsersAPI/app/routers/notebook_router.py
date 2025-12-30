from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db

from ..schemas.source_schema import SourceOut
from ..schemas.notebook_schema import NotebookCreate, NotebookOut

from ..crud.notebook_crud import create_notebook, get_notebook, get_all_notebooks, delete_notebook, get_all_sources_by_notebook_id, get_all_notebooks_by_user_id


# Creamos el router para agrupar estas rutas
router = APIRouter(
    prefix="/notebooks",
    tags=["notebooks"]
)


@router.post("/", response_model=NotebookOut, status_code=status.HTTP_201_CREATED)
def create_notebook(notebook: NotebookCreate, db: Session = Depends(get_db)):
    """Método para crear un nuevo notebook."""    
    return create_notebook(db=db, notebook=notebook)

@router.get("/", response_model=List[NotebookOut], status_code=status.HTTP_200_OK)
def read_notebooks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Método para obtener todos los notebooks con paginación."""
    notebooks = get_all_notebooks(db, skip=skip, limit=limit)

    return notebooks


@router.get("/{notebook_id}", response_model=NotebookOut, status_code=status.HTTP_200_OK)
def read_notebook(notebook_id: int, db: Session = Depends(get_db)):
    """Método para obtener un notebook por su ID."""
    notebook = get_notebook(db, notebook_id=notebook_id)

    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook no encontrado")
    
    return notebook


@router.delete("/{notebook_id}", response_model=NotebookOut, status_code=status.HTTP_200_OK)
def delete_notebook(notebook_id: int, db: Session = Depends(get_db)):
    """Método para eliminar un notebook por su ID."""
    notebook = get_notebook(db, notebook_id=notebook_id)

    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook no encontrado")
    
    notebook = delete_notebook(db, notebook_id=notebook_id)

    return notebook

@router.get("/{notebook_id}/sources", response_model=List[SourceOut], status_code=status.HTTP_200_OK)
def read_sources_by_notebook_id(notebook_id: int, db: Session = Depends(get_db)):
    """Método para obtener las fuentes (sources) asociadas a un notebook específico."""
    notebook = get_notebook(db, notebook_id=notebook_id)
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook no encontrado")

    sources = get_all_sources_by_notebook_id(db, notebook_id=notebook_id)

    if not sources:
        raise HTTPException(status_code=404, detail="Fuentes no encontradas para este notebook")
    
    return sources

@router.get("/user/{user_id}", response_model=List[NotebookOut], status_code=status.HTTP_200_OK)
def read_notebooks_by_user_id(user_id: int, db: Session = Depends(get_db)):
    """Método para obtener los notebooks asociados a un usuario específico."""
    notebooks = get_all_notebooks_by_user_id(db, user_id=user_id)

    if not notebooks:
        raise HTTPException(status_code=404, detail="No se encontraron notebooks para este usuario")
    
    return notebooks