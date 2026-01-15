from pydantic import BaseModel
from typing import List


class ContextRequest(BaseModel):
    query: str
    filter : str


class RAGRequest(BaseModel):
    question: str
    pdf_ids: List[int]
    filter: str = ""


class RAGResponse(BaseModel):
    question: str
    generation: str
    context: str
    is_valid: bool
    refinement_attempts: int
