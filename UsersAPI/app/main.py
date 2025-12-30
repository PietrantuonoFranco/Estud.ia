from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine

# Routers
from .routers.user_router import router as users_router
from .routers.notebook_router import router as notebooks_router
from .routers.source_router import router as sources_router
from .routers.auth_router import router as auth_router

# Models
from .models.user_model import User
from .models.notebook_model import Notebook
from .models.source_model import Source

User.metadata.create_all(bind=engine)
Notebook.metadata.create_all(bind=engine)
Source.metadata.create_all(bind=engine)

app = FastAPI()

# 1. Define la lista de orígenes permitidos
origins = [
    "http://localhost:3000",
]

# 2. Agrega el middleware a la aplicación
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Lista de URLs permitidas
    allow_credentials=True,           # Permite el envío de cookies y tokens
    allow_methods=["*"],              # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],              # Permite todos los encabezados
)

app.include_router(users_router)
app.include_router(notebooks_router)
app.include_router(sources_router)
app.include_router(auth_router)