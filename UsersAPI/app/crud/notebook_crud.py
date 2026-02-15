from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from ..schemas.notebook_schema import NotebookCreate
from ..models.source_model import Source
from ..models.notebook_model import Notebook
from ..models.quiz_model import Quiz

# --- FUNCIONES AUXILIARES ---

async def _load_notebook_with_relations(db: AsyncSession, notebook_id: int):
    """Función auxiliar para cargar un notebook con todas sus relaciones eagerly."""
    query = (
        select(Notebook)
        .options(
            joinedload(Notebook.messages),
            joinedload(Notebook.sources),
            joinedload(Notebook.flashcards),
            joinedload(Notebook.quizzes),
        )
        .filter(Notebook.id == notebook_id)
    )
    result = await db.execute(query)
    return result.unique().scalars().first()

# --- OPERACIONES DE NOTEBOOKS ---

async def create_notebook(db: AsyncSession, notebook: NotebookCreate, auto_commit: bool = True):
    """Crea un nuevo notebook en la base de datos de forma asíncrona."""
    db_notebook = Notebook(
        title=notebook.title,
        icon=notebook.icon,
        description=notebook.description,
        user_id=notebook.user_id,
    )

    db.add(db_notebook)
    await db.flush()  # Genera el ID sin hacer commit
    await db.refresh(db_notebook)  # Obtiene el ID generado
    
    if auto_commit:
        await db.commit()
    return db_notebook

async def get_all_notebooks(db: AsyncSession, skip: int = 0, limit: int = 10):
    """Obtener notebooks con todas sus relaciones cargadas."""
    query = (
        select(Notebook)
        .options(
            joinedload(Notebook.sources),
            joinedload(Notebook.messages),
            joinedload(Notebook.flashcards),
            joinedload(Notebook.quizzes).joinedload(Quiz.questions)
        )
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    return result.scalars().unique().all()

async def get_notebook(db: AsyncSession, notebook_id: int):
    """Obtener un notebook por su ID con todas sus relaciones."""
    query = (
        select(Notebook)
        .options(
            joinedload(Notebook.messages),
            joinedload(Notebook.sources),
            joinedload(Notebook.flashcards),
            joinedload(Notebook.quizzes).joinedload(Quiz.questions)
        )
        .filter(Notebook.id == notebook_id)
    )
    result = await db.execute(query)
    return result.scalars().unique().first()

async def delete_notebook(db: AsyncSession, notebook_id: int):
    """Eliminar un notebook de forma asíncrona."""
    # Primero buscamos el objeto
    query = select(Notebook).filter(Notebook.id == notebook_id)
    result = await db.execute(query)
    db_notebook = result.scalars().first()
    
    if db_notebook:
        await db.delete(db_notebook)
        await db.commit()
    return db_notebook


# --- OPERACIONES DE SOURCES ---

async def get_all_sources_by_notebook_id(db: AsyncSession, notebook_id: int):
    query = select(Source).filter(Source.notebook_id == notebook_id)
    result = await db.execute(query)
    return result.scalars().all()


# --- OPERACIONES DE USER ---
async def get_all_notebooks_by_user_id(db: AsyncSession, user_id: int):
    """Obtener todos los notebooks de un usuario con todas sus relaciones cargadas."""
    query = (
        select(Notebook)
        .filter(Notebook.user_id == user_id)
        .options(
            joinedload(Notebook.sources),
            joinedload(Notebook.messages),
            joinedload(Notebook.flashcards),
            joinedload(Notebook.quizzes).joinedload(Quiz.questions)
        )
    )
    result = await db.execute(query)
    return result.scalars().unique().all()