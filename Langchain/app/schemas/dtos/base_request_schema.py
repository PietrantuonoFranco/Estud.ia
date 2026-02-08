from pydantic import BaseModel
from typing import List


class BaseRequest(BaseModel):
    pdf_ids: List[int]
    filter: str = ""