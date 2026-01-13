from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List
import httpx

from ..config import conf
from ..database import get_db
from ..schemas.source_schema import SourceCreate, SourceOut
from ..schemas.notebook_schema import NotebookOut
from ..crud.source_crud import (
    create_source as create_source_crud,
    get_source,
    get_all_sources,
    delete_source as delete_source_crud,
    get_notebook_by_source,
)


# Creamos el router para agrupar estas rutas
router = APIRouter(
    prefix="/sources",
    tags=["sources"]
)

http_client = httpx.AsyncClient()

@router.on_event("startup")
async def startup_event():
    pass

@router.on_event("shutdown")
async def shutdown_event():
    await http_client.aclose()

@router.post("/", response_model=SourceOut, status_code=status.HTTP_201_CREATED)
def create_source(source: SourceCreate, db: Session = Depends(get_db)):
    """Método para crear una nueva fuente (source)."""    
    return create_source_crud(db=db, source=source)


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


@router.delete("/delete-various", response_model=List[SourceOut], status_code=status.HTTP_200_OK)
async def delete_various_sources(
    body: dict = Body(...),
    db: Session = Depends(get_db)
):
    """Método para eliminar varias fuentes (sources) por sus IDs."""
    pdf_ids = body.get("pdf_ids", [])
    
    if not pdf_ids or not isinstance(pdf_ids, list):
        raise HTTPException(status_code=400, detail="pdf_ids must be a non-empty list")
    
    try:
        response = await http_client.post(
            f"{conf.LANGCHAIN_URI}/delete-pdfs",
            json={"pdf_ids": pdf_ids}, # Enviamos todo aquí
            headers={"X-API-Key": conf.LANGCHAIN_API_KEY},
            timeout=60.0
        )
        response.raise_for_status()

    except httpx.HTTPStatusError as e:
        print(f"HTTPStatusError: {e.response.status_code} - {e.response.text}")
        raise HTTPException(status_code=e.response.status_code, detail=f"Has occurred an error with Langchain service: {e.response.text}")
        
    except Exception as e:
        print(f"Connection Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Connection Error: {str(e)}")

    deleted_sources = []

    for source_id in pdf_ids:
        source = get_source(db, source_id=source_id)

        if not source:
            raise HTTPException(status_code=404, detail="Source not found")

        source = delete_source_crud(db, source_id=source_id)

        deleted_sources.append(source)

    return deleted_sources


@router.delete("/{source_id}", response_model=SourceOut, status_code=status.HTTP_200_OK)
async def delete_source(source_id: int, db: Session = Depends(get_db)):
    """Método para eliminar una fuente (source) por su ID."""
    source = get_source(db, source_id=source_id)

    if not source:
        raise HTTPException(status_code=404, detail="Fuente no encontrada")

    pdf_ids = []
    pdf_ids.append(source_id)


    try:
        response = await http_client.post(
            f"{conf.LANGCHAIN_URI}/delete-pdfs",
            json={"pdf_ids": pdf_ids}, # Enviamos todo aquí
            headers={"X-API-Key": conf.LANGCHAIN_API_KEY},
            timeout=60.0
        )

        response.raise_for_status()
    
    except httpx.HTTPStatusError as e:
        print(f"HTTPStatusError: {e.response.status_code} - {e.response.text}")
        raise HTTPException(status_code=e.response.status_code, detail=f"Has occurred an error with Langchain service: {e.response.text}")
        
    except Exception as e:
        print(f"Connection Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Connection Error: {str(e)}")  

    source = delete_source_crud(db, source_id=source_id)

    return source


@router.get("/{source_id}/notebook", response_model=NotebookOut, status_code=status.HTTP_200_OK)
def read_notebook_by_source(source_id: int, db: Session = Depends(get_db)):
    """Método para obtener el notebook asociado a una fuente (source) específica."""
    notebook = get_notebook_by_source(db, source_id=source_id)

    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook no encontrado para esta fuente")
    
    return notebook