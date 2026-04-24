from pydantic import BaseModel

class Citation(BaseModel):
    source: str
    page: int

class Answer(BaseModel):
    text: str
    citations: list[Citation] = []
