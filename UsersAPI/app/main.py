from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from .database import engine

from .config import conf

# Routers
from .routers.user_router import router as users_router
from .routers.notebook_router import router as notebooks_router
from .routers.source_router import router as sources_router
from .routers.auth_router import router as auth_router
from .routers.message_router import router as messages_router
from .routers.summary_router import router as summaries_router
from .routers.flashcard_router import router as flashcards_router
from .routers.quiz_router import router as quizzes_router

# Models
from .models.user_model import User
from .models.notebook_model import Notebook
from .models.source_model import Source
from .models.message_model import Message
from .models.summary_model import Summary
from .models.flashcard_model import Flashcard
from .models.quiz_model import Quiz
from .models.questions_and_answers_model import QuestionsAndAnswers

User.metadata.create_all(bind=engine)
Notebook.metadata.create_all(bind=engine)
Source.metadata.create_all(bind=engine)
Message.metadata.create_all(bind=engine)
Summary.metadata.create_all(bind=engine)
Flashcard.metadata.create_all(bind=engine)
Quiz.metadata.create_all(bind=engine)
QuestionsAndAnswers.metadata.create_all(bind=engine)

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
app.add_middleware(SessionMiddleware, secret_key=conf.SECRET_KEY)

app.include_router(users_router)
app.include_router(notebooks_router)
app.include_router(sources_router)
app.include_router(auth_router)
app.include_router(messages_router)
app.include_router(summaries_router)
app.include_router(flashcards_router)
app.include_router(quizzes_router)