from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from typing import List
import httpx
import datetime as date

from ..config import conf
from ..database import get_db
from ..schemas.notebook_schema import NotebookOut, NotebookCreate
from ..schemas.source_schema import SourceOut, SourceCreate
from ..models.source_model import Source
from ..security.auth import get_current_user
from ..crud.source_crud import create_source
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
    pass

@router.on_event("shutdown")
async def shutdown_event():
    await http_client.aclose()


@router.post("/", response_model=NotebookOut, status_code=status.HTTP_201_CREATED)
async def create_notebook(files: List[UploadFile], db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Método para crear un nuevo notebook."""
    
    try:
        # Validar tipos de archivo y crear sources en DB
        source_ids = []
        file_contents = []
        
        for file in files:
            if not file.filename.lower().endswith(('.pdf')):
                raise HTTPException(status_code=400, detail="Invalid file type. Only PDFs are allowed.")
            
            # Leer el contenido del archivo
            content = await file.read()
            file_contents.append((file.filename, file.content_type, content))
            
            source_data = SourceCreate(
                name=file.filename,
                notebook_id=None
            )

            new_file = create_source(db=db, source=source_data)
            source_ids.append(new_file.id)

        # Preparar TODO en una sola lista para el parámetro files
        multipart_data = []

        for (filename, content_type, content), source_id in zip(file_contents, source_ids):
            # Agregar el archivo
            multipart_data.append(('files', (filename, content, content_type)))
            # Agregar el ID como un campo de formulario simple
            multipart_data.append(('source_ids', (None, str(source_id)))) # None indica que no es un archivo

        try:
            response = await http_client.post(
                f"{conf.LANGCHAIN_URI}/create-notebook",
                files=multipart_data, # Enviamos todo aquí
                headers={"X-API-Key": conf.LANGCHAIN_API_KEY},
                timeout=60.0
            )
            response.raise_for_status()


            response.raise_for_status() # Lanza error si la API externa falla

        except httpx.HTTPStatusError as e:
            print(f"HTTPStatusError: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"Error en servicio externo de Langchain: {e.response.text}")
        
        except Exception as e:
            print(f"Connection Error: {str(e)}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Error de conexión: {str(e)}")

        # 3. Procesar respuesta como Diccionario y normalizar longitudes para evitar truncamientos en DB
        notebook_response = response.json()

        # Enforce column length limits according to model/DB: title(60), icon(45), description(512)
        title = str(notebook_response.get("title", ""))[:60]
        icon = str(notebook_response.get("icon", ""))[:45]
        description = str(notebook_response.get("description", ""))[:512]
        
        # 4. Crear objeto NotebookCreate con los datos de Langchain + datos del usuario
        notebook_data = NotebookCreate(
            title=title,
            icon=icon,
            description=description,
            date=date.datetime.now().date(),
            user_id=current_user.id
        )

        # 5. Crear en base de datos local
        new_notebook = create_notebook_crud(db=db, notebook=notebook_data)


        # 6. Asociar las fuentes (sources) al notebook creado
        for source_id in source_ids:
            source = db.query(Source).filter(Source.id == source_id).first()
            if source:
                source.notebook_id = new_notebook.id
                db.add(source)
        db.commit()
        
        # Recargar el notebook con todas sus relaciones
        db.refresh(new_notebook)
        
        return new_notebook
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error in create_notebook: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

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