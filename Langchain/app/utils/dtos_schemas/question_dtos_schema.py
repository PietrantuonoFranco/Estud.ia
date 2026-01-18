from pydantic import BaseModel

class QuestionResponse(BaseModel):
    question: str
    answer: str
    incorrect_answer_1: str
    incorrect_answer_2: str
    incorrect_answer_3: str