from fastapi import FastAPI

from .database import engine

# Routers
from .routers.user_router import router as users_router
from .routers.notebook_router import router as notebooks_router
from .routers.source_router import router as sources_router

# Models
from .models.user_model import User
from .models.notebook_model import Notebook
from .models.source_model import Source

User.metadata.create_all(bind=engine)
Notebook.metadata.create_all(bind=engine)
Source.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router)
app.include_router(notebooks_router)
app.include_router(sources_router)