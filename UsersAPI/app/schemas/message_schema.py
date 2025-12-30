from pydantic import BaseModel


class MessageBase(BaseModel):
    text: str
    notebook_id: int
    notebook_users_id: int
    is_user_message: bool = True


class MessageCreate(MessageBase):
    pass


class MessageOut(MessageBase):
    id: int

    class Config:
        from_attributes = True
