from sqlalchemy.orm import Session  # Importamos la función de hash_password

from ..schemas.source_schema import SourceCreate

from ..source_model import Source
from ..notebook_model import Notebook


def create_source(db: Session, source: SourceCreate):
    """Crea una nueva fuente (source) en la base de datos."""
    db_source = Source(
        pdf_file=source.pdf_file,
        notebook_id=source.notebook_id,
    )

    db.add(db_source)
    db.commit()
    db.refresh(db_source)

    return db_source

def get_all_sources(db: Session, skip: int = 0, limit: int = 10):
    """Obtener todas las fuentes (sources) con paginación."""
    return db.query(Source).offset(skip).limit(limit).all()

def get_source(db: Session, source_id: int):
    """Obtener una fuente (source) por su ID."""
    return db.query(Source).filter(Source.id == source_id).first()

def delete_source(db: Session, source_id: int):
    """Eliminar una fuente (source) por su ID."""
    db_source = db.query(Source).filter(Source.id == source_id).first()
    if db_source:
        db.delete(db_source)
        db.commit()
    return db_source


# --- OPERACIONES DE NOTEBOOK ---

def get_notebook_by_source(db: Session, source_id: int):
    """Obtener el notebook asociado a una fuente (source) específica."""
    return db.query(Notebook).filter(Notebook.sources_id == source_id).first()