from pydantic import BaseModel
from typing import Optional
from fastapi_users import schemas
import uuid

class PostCreate(BaseModel):
    title: str
    content: str

class DeletePost(BaseModel):
    id: int
    title: Optional[str] = None

class PostResponse(BaseModel):
    title: str
    content: str


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UseUpdate(schemas.BaseUserUpdate):
    pass