from sqlalchemy.orm import Session  # Importamos la función de hash_password

from ..schemas.source_schema import SourceCreate

from ..source_model import Source
from ..notebook_model import Notebook


def create_notebook(db: Session, notebook: SourceCreate):
    """Crea un nuevo notebook (cuaderno) en la base de datos."""
    db_source = Notebook(
        title=notebook.title,
        icon=notebook.icon,
        date=notebook.date,
        collection_name=notebook.collection_name,
        users_id=notebook.users_id
    )

    db.add(db_source)
    db.commit()
    db.refresh(db_source)

    return db_source

def get_all_notebooks(db: Session, skip: int = 0, limit: int = 10):
    """Obtener todas las fuentes (sources) con paginación."""
    return db.query(Notebook).offset(skip).limit(limit).all()

def get_notebook(db: Session, notebook_id: int):
    """Obtener un notebook (cuaderno) por su ID."""
    return db.query(Notebook).filter(Notebook.id == notebook_id).first()

def delete_notebook(db: Session, notebook_id: int):
    """Eliminar un notebook (cuaderno) por su ID."""
    db_notebook = db.query(Notebook).filter(Notebook.id == notebook_id).first()
    if db_notebook:
        db.delete(db_notebook)
        db.commit()
    return db_notebook


# --- OPERACIONES DE SOURCES ---

def get_all_sources_by_notebook_id(db: Session, notebook_id: int):
    """Obtener todas las fuentes (sources) asociadas a un notebook específico."""
    return db.query(Source).filter(Source.notebook_id == notebook_id).all()


# --- OPERACIONES DE USER ---
def get_all_notebooks_by_user_id(db: Session, user_id: int):
    """Obtener todos los notebooks (cuadernos) asociados a un usuario específico."""
    return db.query(Notebook).filter(Notebook.users_id == user_id).all()