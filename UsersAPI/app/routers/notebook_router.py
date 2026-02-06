from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Body
from sqlalchemy.orm import Session
from typing import List
import httpx
import datetime as date

from ..config import conf
from ..database import get_db
from ..schemas.notebook_schema import NotebookOut, NotebookCreate
from ..schemas.source_schema import SourceOut, SourceCreate
from ..schemas.flashcard_schema import FlashcardCreate, FlashcardOut
from ..schemas.quiz_schema import QuizWithQuestions, QuizCreate, QuestionCreate
from ..models.source_model import Source
from ..security.auth import get_current_user
from ..crud.source_crud import create_source, get_source, delete_source as delete_source_crud
from ..crud.flashcard_crud import create_flashcard
from ..crud.quiz_crud import create_quiz
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

            new_file = await create_source(db=db, source=source_data)
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

        except httpx.HTTPStatusError as e:
            # Limpieza: eliminar sources creados si Langchain falla
            try:
                for source_id in source_ids:
                    await delete_source_crud(db, source_id=source_id)
                db.commit()
            finally:
                pass
            print(f"HTTPStatusError: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"Error en servicio externo de Langchain: {e.response.text}")
        
        except Exception as e:
            # Limpieza: eliminar sources creados si hay error de conexión
            try:
                for source_id in source_ids:
                    await delete_source_crud(db, source_id=source_id)
                db.commit()
            finally:
                pass
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
        new_notebook = await create_notebook_crud(db=db, notebook=notebook_data)


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
    return await get_all_notebooks(db, skip=skip, limit=limit)


@router.get("/{notebook_id}", response_model=NotebookOut, status_code=status.HTTP_200_OK)
async def read_notebook(notebook_id: int, db: Session = Depends(get_db)):
    """Método para obtener un notebook por su ID."""
    notebook = await get_notebook_crud(db, notebook_id=notebook_id)

    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook no encontrado")
    
    return notebook

@router.delete("/{notebook_id}", response_model=NotebookOut, status_code=status.HTTP_200_OK)
async def delete_notebook(notebook_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Método para eliminar un notebook por su ID."""
    notebook = await get_notebook_crud(db, notebook_id=notebook_id)

    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook no encontrado")
    
    if notebook.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar este notebook")
    
    return await delete_notebook_crud(db, notebook_id=notebook_id)

@router.get("/{notebook_id}/sources", response_model=List[SourceOut], status_code=status.HTTP_200_OK)
async def read_sources_by_notebook_id(notebook_id: int, db: Session = Depends(get_db)):
    """Método para obtener las fuentes (sources) asociadas a un notebook específico."""
    notebook = await get_notebook_crud(db, notebook_id=notebook_id)
    
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook no encontrado")

    sources = await get_all_sources_by_notebook_id(db, notebook_id=notebook_id)

    if not sources:
        raise HTTPException(status_code=404, detail="Fuentes no encontradas para este notebook")
    
    return sources

@router.get("/user/{user_id}", response_model=List[NotebookOut], status_code=status.HTTP_200_OK)
async def read_notebooks_by_user_id(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Método para obtener los notebooks asociados a un usuario específico."""
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver los notebooks de este usuario")
    
    notebooks = await get_all_notebooks_by_user_id(db, user_id=user_id)

    if not notebooks:
        raise HTTPException(status_code=404, detail="No se encontraron notebooks para este usuario")
    
    return notebooks

@router.post("/{notebook_id}/sources", response_model=NotebookOut, status_code=status.HTTP_200_OK)
async def add_sources_to_notebook(notebook_id: int, files: List[UploadFile] = File(...), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Método para agregar fuentes a un notebook."""

    notebook = await get_notebook_crud(db, notebook_id=notebook_id)

    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")
    
    if notebook.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para agregar fuentes a este notebook")
    
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

            new_file = await create_source(db=db, source=source_data)
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
                f"{conf.LANGCHAIN_URI}/upload-pdfs",
                files=multipart_data, # Enviamos todo aquí
                headers={"X-API-Key": conf.LANGCHAIN_API_KEY},
                timeout=60.0
            )
            
            response.raise_for_status()

        except httpx.HTTPStatusError as e:
            # Limpieza: eliminar sources creados si Langchain falla
            try:
                for source_id in source_ids:
                    await delete_source_crud(db, source_id=source_id)
                db.commit()
            finally:
                pass
            print(f"HTTPStatusError: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"An error has occurred with Langchain service: {e.response.text}")
        
        except Exception as e:
            # Limpieza: eliminar sources creados si hay error de conexión
            try:
                for source_id in source_ids:
                    await delete_source_crud(db, source_id=source_id)
                db.commit()
            finally:
                pass
            print(f"Connection Error: {str(e)}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Connection error: {str(e)}")

        # 6. Asociar las fuentes (sources) al notebook creado
        for source_id in source_ids:
            source = db.query(Source).filter(Source.id == source_id).first()

            if source:
                source.notebook_id = notebook.id
                db.add(source)

        db.commit()
        
        # Recargar el notebook con todas sus relaciones
        db.refresh(notebook)
        
        return notebook
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error in add_sources_to_notebook: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.post("/{notebook_id}/flashcards", response_model=List[FlashcardOut], status_code=status.HTTP_200_OK)
async def add_flashcards_to_notebook(notebook_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        notebook = await get_notebook_crud(db, notebook_id=notebook_id)

        if not notebook:
            raise HTTPException(status_code=404, detail="Notebook not found")
        
        if notebook.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="No tienes permiso para agregar flashcards a este notebook")
        
        print(f"Notebook found: {notebook.title}, source_ids: {[source.id for source in notebook.sources]}")
        
        if not notebook.sources or len(notebook.sources) == 0:
            raise HTTPException(status_code=400, detail="Notebook has no sources to generate flashcards from")
        
        # Convert source_ids to integers
        pdf_ids = [source.id for source in notebook.sources]
        
        print(f"Sending request to Langchain with pdf_ids: {pdf_ids}")
        
        try:
            response = await http_client.post(
                f"{conf.LANGCHAIN_URI}/create-flashcards",
                json={"pdf_ids": pdf_ids},
                headers={"X-API-Key": conf.LANGCHAIN_API_KEY},
                timeout=60.0
            )
            
            response.raise_for_status()
            print(f"Langchain response status: {response.status_code}")

        except httpx.HTTPStatusError as e:
            print(f"HTTPStatusError: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"An error has occurred with Langchain service: {e.response.text}")
        
        except Exception as e:
            print(f"Connection Error: {str(e)}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Connection error: {str(e)}")

        flashcard_response = response.json()
        print(f"Flashcard response: {flashcard_response}")

        new_flashcards = []
      
        for fc in flashcard_response.get("flashcards", []):
            new_flashcard = FlashcardCreate(
                question=fc["question"],
                answer=fc["answer"],
                notebook_id=notebook_id,
                notebook_users_id=notebook.user_id
            )

            new_flashcards.append(await create_flashcard(db=db, flashcard=new_flashcard))

        print(f"Created {len(new_flashcards)} flashcards")
        return new_flashcards
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error in add_flashcards_to_notebook: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
@router.post("/{notebook_id}/quiz", response_model=QuizWithQuestions, status_code=status.HTTP_200_OK)
async def add_quiz_to_notebook(notebook_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        notebook = await get_notebook_crud(db, notebook_id=notebook_id)

        if not notebook:
            raise HTTPException(status_code=404, detail="Notebook not found")
        
        if notebook.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="No tienes permiso para agregar un quiz a este notebook")
        
        if not notebook.sources or len(notebook.sources) == 0:
            raise HTTPException(status_code=400, detail="Notebook has no sources to generate flashcards from")
        
        # Convert source_ids to integers
        pdf_ids = [source.id for source in notebook.sources]
        
        try:
            response = await http_client.post(
                f"{conf.LANGCHAIN_URI}/create-questions-and-answers",
                json={"pdf_ids": pdf_ids},
                headers={"X-API-Key": conf.LANGCHAIN_API_KEY},
                timeout=60.0
            )
            
            response.raise_for_status()

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"An error has occurred with Langchain service: {e.response.text}")
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Connection error: {str(e)}")

        questions_response = response.json()
        print(f"Questions response: {questions_response}")

        # Extract title from response
        quiz_title = questions_response.get("title", "Untitled Quiz")[:255]

        # Build question payloads (do not set quiz_id yet)
        new_questions = []
        for q in questions_response.get("question_and_answers", []):
            new_question = QuestionCreate(
                question=q.get("question"),
                answer=q.get("answer"),
                incorrect_answer_1=q.get("incorrect_answer_1", ""),
                incorrect_answer_2=q.get("incorrect_answer_2", ""),
                incorrect_answer_3=q.get("incorrect_answer_3", ""),
            )
            new_questions.append(new_question)

        # Create quiz with questions in DB
        quiz_payload = QuizCreate(
            title=quiz_title,
            notebook_id=int(notebook_id),
            notebook_users_id=current_user.id,
            questions=new_questions,
        )

        created_quiz = await create_quiz(db, quiz_payload)

        # Prepare response matching QuizWithQuestions
        questions_out = []
        for qq in created_quiz.questions:
            questions_out.append({
                "id": qq.id,
                "question": qq.question,
                "answer": qq.answer,
                "incorrect_answer_1": qq.incorrect_answer_1,
                "incorrect_answer_2": qq.incorrect_answer_2,
                "incorrect_answer_3": qq.incorrect_answer_3,
                "quiz_id": qq.quiz_id,
            })

        response_body = {
            "id": created_quiz.id,
            "notebook_id": created_quiz.notebook_id,
            "notebook_users_id": created_quiz.notebook_users_id,
            "title": created_quiz.title,
            "questions_and_answers": questions_out,
        }

        print(f"Created quiz id={created_quiz.id} with {len(questions_out)} questions")
        return response_body
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error in add_quiz_to_notebook: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/{notebook_id}/sources", response_model=List[SourceOut], status_code=status.HTTP_200_OK)
async def delete_various_sources(
    notebook_id: int,
    body: dict = Body(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Método para eliminar varias fuentes (sources) por sus IDs."""

    notebook = await get_notebook_crud(db, notebook_id=notebook_id)

    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")
        
    if notebook.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar fuentes de este notebook")

    pdf_ids = body.get("pdf_ids", [])

    if len(notebook.sources) <= len(pdf_ids):
        raise HTTPException(status_code=400, detail="Cannot delete all sources from the notebook")
    
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
        source = await get_source(db, source_id=source_id)

        if not source:
            raise HTTPException(status_code=404, detail="Source not found")

        source = await delete_source_crud(db, source_id=source_id)

        deleted_sources.append(source)

    return deleted_sources