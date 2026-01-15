from pydantic import BaseModel, UploadFile


class SourceRequest(BaseModel):
    id: int
    file: UploadFile

class NotebookResponse(BaseModel):
    title: str
    icon: str
    description: str