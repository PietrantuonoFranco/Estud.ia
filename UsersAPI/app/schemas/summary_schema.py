from pydantic import BaseModel


class SummaryBase(BaseModel):
    text: str
    notebook_id: int
    notebook_users_id: int


class SummaryCreate(SummaryBase):
    pass


class SummaryOut(SummaryBase):
    id: int

    class Config:
        from_attributes = True
