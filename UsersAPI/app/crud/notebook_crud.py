from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy import delete as sql_delete

from ..schemas.notebook_schema import NotebookCreate
from ..models.source_model import Source
from ..models.notebook_model import Notebook
from ..models.quiz_model import Quiz
from ..models.message_model import Message
from ..models.flashcard_model import Flashcard
from ..models.summary_model import Summary
from ..models.questions_and_answers_model import QuestionsAndAnswers

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
    """Eliminar un notebook y todas sus entidades relacionadas de forma asíncrona."""
    # Primero verificamos que el notebook existe (sin cargar el objeto ORM)
    check_query = select(Notebook.id).filter(Notebook.id == notebook_id)
    result = await db.execute(check_query)
    notebook_exists = result.scalar_one_or_none()
    
    if not notebook_exists:
        return None
    
    # Obtener los IDs de los quizzes para eliminar sus preguntas
    quiz_query = select(Quiz.id).filter(Quiz.notebook_id == notebook_id)
    quiz_result = await db.execute(quiz_query)
    quiz_ids = quiz_result.scalars().all()
    
    # 1. Eliminar preguntas de los quizzes
    if quiz_ids:
        await db.execute(
            sql_delete(QuestionsAndAnswers).where(QuestionsAndAnswers.quiz_id.in_(quiz_ids))
        )
    
    # 2. Eliminar messages
    await db.execute(
        sql_delete(Message).where(Message.notebook_id == notebook_id)
    )
    
    # 3. Eliminar sources
    await db.execute(
        sql_delete(Source).where(Source.notebook_id == notebook_id)
    )
    
    # 4. Eliminar flashcards
    await db.execute(
        sql_delete(Flashcard).where(Flashcard.notebook_id == notebook_id)
    )
    
    # 5. Eliminar summaries
    await db.execute(
        sql_delete(Summary).where(Summary.notebook_id == notebook_id)
    )
    
    # 6. Eliminar quizzes
    await db.execute(
        sql_delete(Quiz).where(Quiz.notebook_id == notebook_id)
    )
    
    # 7. Finalmente, eliminar el notebook
    await db.execute(
        sql_delete(Notebook).where(Notebook.id == notebook_id)
    )
    await db.commit()
    
    return True


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