from pydantic import BaseModel
from typing import List

class Flashcard(BaseModel):
    question: str
    answer: str

class FlashcardRequest(BaseModel):
    pdf_ids: List[int]
    filter: str = ""

class FlashcardResponse(BaseModel):
    flashcards: list[Flashcard]