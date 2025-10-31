from pydantic import BaseModel
from typing import Optional


class PostCreate(BaseModel):
    title: str
    content: str

class DeletePost(BaseModel):
    id: int
    title: Optional[str] = None

class PostResponse(BaseModel):
    title: str
    content: str
