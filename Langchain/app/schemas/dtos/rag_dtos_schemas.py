from pydantic import BaseModel

from .base_request_schema import BaseRequest

class ContextRequest(BaseModel):
    query: str
    filter : str


class RAGRequest(BaseRequest):
    question: str
    chatHistory: list[dict]


class RAGResponse(BaseModel):
    question: str
    generation: str
    context: str
    is_valid: bool
    refinement_attempts: int
