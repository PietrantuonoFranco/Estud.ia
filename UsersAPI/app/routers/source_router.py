from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import SessionLocal

from ..schemas.source_schema import SourceCreate, SourceOut
from ..schemas.notebook_schema import NotebookOut

from ..crud.source_crud import create_source, get_source, get_all_sources, delete_source, get_notebook_by_source


# Creamos el router para agrupar estas rutas
router = APIRouter(
    prefix="/sources",
    tags=["sources"]
)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=SourceOut, status_code=status.HTTP_201_CREATED)
def create_source(source: SourceCreate, db: Session = Depends(get_db)):
    """Método para crear una nueva fuente (source)."""    
    return create_source(db=db, source=source)


@router.get("/", response_model=List[SourceOut], status_code=status.HTTP_200_OK)
def read_sources(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Método para obtener todas las fuentes (sources) con paginación."""
    sources = get_all_sources(db, skip=skip, limit=limit)

    return sources


@router.get("/{source_id}", response_model=SourceOut, status_code=status.HTTP_200_OK)
def read_source(source_id: int, db: Session = Depends(get_db)):
    """Método para obtener una fuente (source) por su ID."""
    source = get_source(db, source_id=source_id)

    if not source:
        raise HTTPException(status_code=404, detail="Fuente no encontrada")
    
    return source


@router.delete("/{source_id}", response_model=SourceOut, status_code=status.HTTP_200_OK)
def delete_source(source_id: int, db: Session = Depends(get_db)):
    """Método para eliminar una fuente (source) por su ID."""
    source = get_source(db, source_id=source_id)

    if not source:
        raise HTTPException(status_code=404, detail="Fuente no encontrada")
    
    source = delete_source(db, source_id=source_id)

    return source


@router.get("/{source_id}/notebook", response_model=NotebookOut, status_code=status.HTTP_200_OK)
def read_notebook_by_source(source_id: int, db: Session = Depends(get_db)):
    """Método para obtener el notebook asociado a una fuente (source) específica."""
    notebook = get_notebook_by_source(db, source_id=source_id)

    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook no encontrado para esta fuente")
    
    return notebook