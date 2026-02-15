from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .config import conf

# 1. Usamos create_async_engine en lugar de create_engine
engine = create_async_engine(
    conf.DB_URL,
    echo=True, # Útil para debug, puedes quitarlo en producción
    future=True,
    connect_args={"statement_cache_size": 0},
)

# 2. Usamos async_sessionmaker para manejar sesiones asíncronas
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False, # Importante en async para evitar errores al acceder a atributos después de un commit
)

Base = declarative_base()

# 3. La dependencia get_db ahora debe ser una función asíncrona
async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()