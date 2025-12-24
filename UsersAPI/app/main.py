from fastapi import FastAPI

# Routers
from .routers.user_router import router as users_router
from .routers.notebook_router import router as notebooks_router
from .routers.source_router import router as sources_router

app = FastAPI()

app.include_router(users_router)
app.include_router(notebooks_router)
app.include_router(sources_router)