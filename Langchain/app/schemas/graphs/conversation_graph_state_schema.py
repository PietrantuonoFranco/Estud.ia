from .base_graph_state_schema import BaseGraphState

class ConversationGraphState(BaseGraphState):
    """
    ConversationGraph state for managing conversation context
    """
    question: str  # Pregunta original
    query: str  # Query refinada (puede cambiar)