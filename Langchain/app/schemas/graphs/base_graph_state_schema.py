from typing import TypedDict, Annotated
import operator

class BaseGraphState(TypedDict):
    """
    BaseGraph state schema.
    """
    pdf_ids: list[int]  # IDs of PDFs to analyze
    context: str  # Context recovered from all PDFs
    generation: str  # JSON generated with title, icon and description
    
    is_valid: bool  # Si la respuesta es válida según el judge
    refinement_attempts: Annotated[int, operator.add]  # Contador de intentos
    retrieval_attempts: Annotated[int, operator.add]  # Contador de retrieves