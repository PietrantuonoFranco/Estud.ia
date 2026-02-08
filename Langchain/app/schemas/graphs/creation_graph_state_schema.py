from .base_graph_state_schema import BaseGraphState

class CreationGraphState(BaseGraphState):
    """
    CreationGraph state for entities generation
    """
    option: str  # Entity type: "notebook", "source", "flashcard", "quiz"