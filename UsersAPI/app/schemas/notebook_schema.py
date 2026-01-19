from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

from .message_schema import MessageOut
from .source_schema import SourceOut
from .flashcard_schema import FlashcardOut
from .quiz_schema import QuizOut

# --- SCHEMAS DE NOTEBOOK ---

class NotebookBase(BaseModel):
    title: str
    icon: str
    description: str
    date: datetime = Field(default_factory=datetime.now)

class NotebookCreate(NotebookBase):
    user_id: int

class NotebookOut(NotebookBase):
    id: int
    user_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    messages: List[MessageOut] = []
    sources: List[SourceOut] = []
    flashcards: List[FlashcardOut] = []
    quizzes: List[QuizOut] = []

    class Config:
        from_attributes = True