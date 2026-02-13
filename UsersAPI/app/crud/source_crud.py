from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..schemas.source_schema import SourceCreate
from ..models.source_model import Source
from ..models.notebook_model import Notebook


async def create_source(db: AsyncSession, source: SourceCreate):
    """Crea una nueva fuente (source) en la base de datos."""
    db_source = Source(
        name=source.name,
        notebook_id=source.notebook_id,
    )

    db.add(db_source)
    await db.commit()
    await db.refresh(db_source)

    return db_source

async def get_all_sources(db: AsyncSession, skip: int = 0, limit: int = 10):
    """Obtener todas las fuentes (sources) con paginación."""
    query = select(Source).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def get_source(db: AsyncSession, source_id: int):
    """Obtener una fuente (source) por su ID."""
    query = select(Source).filter(Source.id == source_id)
    result = await db.execute(query)
    return result.scalars().first()

async def delete_source(db: AsyncSession, source_id: int):
    """Eliminar una fuente (source) por su ID."""
    db_source = await get_source(db, source_id)
    if db_source:
        await db.delete(db_source)
        await db.commit()
    return db_source


# --- OPERACIONES DE NOTEBOOK ---

async def get_notebook_by_source(db: AsyncSession, source_id: int):
    """Obtener el notebook asociado a una fuente (source) específica."""
    query = select(Notebook).join(Source).filter(Source.id == source_id)
    result = await db.execute(query)
    return result.scalars().first()