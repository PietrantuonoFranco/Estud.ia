from pydantic import BaseModel


class FlashcardBase(BaseModel):
    question: str
    answer: str
    notebook_id: int
    notebook_users_id: int


class FlashcardCreate(FlashcardBase):
    pass


class FlashcardOut(FlashcardBase):
    id: int

    class Config:
        from_attributes = True
